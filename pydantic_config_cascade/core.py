from os import PathLike
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel

from .readers import read_file

PATH_PREFIX = r"${{"
PATH_SUFFIX = r"}}"
BASE_CONFIG_KEY = r"__base__"
REMOVE_KEY = r"__remove__"


def load_model_cascade(data: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, str) and value.startswith(PATH_PREFIX) and value.endswith(PATH_SUFFIX):
            trimmed_path = value.removeprefix(PATH_PREFIX).removesuffix(PATH_SUFFIX).strip()
            value = read_file(trimmed_path)
            data[key] = value

        if isinstance(value, dict):
            data[key] = load_model_cascade(value)

    return data


def update_nested_dict(data: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(updates, dict):
        return updates

    for key, value in updates.items():
        current_value = data.get(key)

        if isinstance(value, str) and value == REMOVE_KEY:
            data.pop(key)
        elif isinstance(current_value, dict) or current_value is None:
            nested_dict = current_value if current_value is not None else dict()
            data[key] = update_nested_dict(nested_dict, value)
        else:
            data[key] = value

    return data


def load_base_config(data: Dict[str, Any], do_nested_update: bool = True) -> Dict[str, Any]:
    if BASE_CONFIG_KEY not in data:
        return data

    base_data = read_file(data[BASE_CONFIG_KEY])

    if do_nested_update:
        base_data = update_nested_dict(base_data, data)
    else:
        base_data.update(data)

    return base_data


class BaseCascadeModel(BaseModel):
    def __init__(self, path_to_file: Optional[Union[str, PathLike[str], Path]] = None, /, **data: Any) -> None:
        if path_to_file is not None:
            data = read_file(path_to_file)

        data = load_model_cascade(data)
        data = load_base_config(data, self.model_config.get("base_nested_update", True))  # type: ignore
        super().__init__(**data)

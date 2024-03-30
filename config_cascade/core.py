from os import PathLike
from pathlib import Path
from typing import Any, Dict, Union

from .readers import read_file

__all__ = [
    "load_config",
    "load_cascaded_configs",
    "load_base_config",
]


PATH_PREFIX = r"${{"
PATH_SUFFIX = r"}}"
BASE_CONFIG_KEY = r"__base__"
REMOVE_KEY = r"__remove__"


def update_nested_dict(data: Dict[str, Any], updates: Any) -> Dict[str, Any]:
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


def load_cascaded_configs(data: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, str) and value.startswith(PATH_PREFIX) and value.endswith(PATH_SUFFIX):
            trimmed_path = value.removeprefix(PATH_PREFIX).removesuffix(PATH_SUFFIX).strip()
            value = read_file(trimmed_path)
            data[key] = value

        if isinstance(value, dict):
            data[key] = load_cascaded_configs(value)

    return data


def load_base_config(data: Dict[str, Any], do_nested_update: bool = True) -> Dict[str, Any]:
    if BASE_CONFIG_KEY not in data:
        return data

    base_data = read_file(data[BASE_CONFIG_KEY])
    base_data = load_cascaded_configs(base_data)

    if do_nested_update:
        base_data = update_nested_dict(base_data, data)
    else:
        base_data.update(data)

    return base_data


def load_config(path_to_file: Union[str, PathLike[str], Path], do_nested_update: bool = True) -> Dict[str, Any]:
    data = read_file(path_to_file)
    data = load_cascaded_configs(data)
    data = load_base_config(data, do_nested_update)

    return data

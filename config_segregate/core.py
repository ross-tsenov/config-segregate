from os import PathLike
from pathlib import Path
from typing import Any, Dict, Union

from .readers import read_file

__all__ = [
    "load_config",
    "load_segregated_configs",
    "load_base_config",
]


PATH_PREFIX = r"${{"
PATH_SUFFIX = r"}}"
BASE_CONFIG_KEY = r"__base__"
DO_NESTED_UPDATE_KEY = r"__do_nested_update__"
REMOVE_KEYS_KEY = r"__remove_keys__"


def update_nested_dict(data: Dict[str, Any], updates: Any) -> Dict[str, Any]:
    if not isinstance(updates, dict):
        return updates

    if REMOVE_KEYS_KEY in updates:
        for remove_key in updates[REMOVE_KEYS_KEY]:
            data.pop(remove_key)

    if not updates.get(DO_NESTED_UPDATE_KEY, True):
        return updates

    for key, value in updates.items():
        current_value = data.get(key)

        if isinstance(current_value, dict):
            data[key] = update_nested_dict(current_value, value)
        else:
            data[key] = value

    return data


def load_segregated_configs(data: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, str) and value.startswith(PATH_PREFIX) and value.endswith(PATH_SUFFIX):
            trimmed_path = value.removeprefix(PATH_PREFIX).removesuffix(PATH_SUFFIX).strip()
            value = read_file(trimmed_path)
            data[key] = value

        if isinstance(value, dict):
            data[key] = load_segregated_configs(value)

    return data


def load_base_config(data: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = load_base_config(value)

    base_data = data.pop(BASE_CONFIG_KEY, None)

    if base_data is not None:
        data = update_nested_dict(base_data, data)

    return data


def load_config(path_to_file: Union[str, PathLike[str], Path]) -> Dict[str, Any]:
    data = read_file(path_to_file)
    data = load_segregated_configs(data)
    data = load_base_config(data)

    return data

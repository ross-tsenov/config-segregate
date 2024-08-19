from os import PathLike
from pathlib import Path
from typing import Any, Dict, Union, TypedDict, List, Hashable

from .readers import read_file

__all__ = [
    "load_config",
    "load_segregated_configs",
    "load_base_config",
]


PATH_PREFIX = r"${{"
PATH_SUFFIX = r"}}"
BASE_CONFIG_KEY = r"__base__"
SEGREGATE_OPTIONS_KEY = r"__segregate_options__"


class SegregateOptions(TypedDict):
    disable_nested_update: bool
    remove_keys: List[Hashable]


def update_nested_dict(data: Dict[Hashable, Any], updates: Any) -> Dict[Hashable, Any]:
    if not isinstance(updates, dict):
        return updates

    segregate_options: SegregateOptions = updates.pop(SEGREGATE_OPTIONS_KEY, {})

    for key_to_remove in segregate_options.get("remove_keys", []):
        data.pop(key_to_remove, None)

    if segregate_options.get("disable_nested_update", False):
        return updates

    # TODO custom handlers go here.

    for key, value in updates.items():
        current_value = data.get(key)

        if isinstance(current_value, dict):
            data[key] = update_nested_dict(current_value, value)
        else:
            data[key] = value

    return data


def load_segregated_configs(data: Any) -> Any:
    if isinstance(data, str) and data.startswith(PATH_PREFIX) and data.endswith(PATH_SUFFIX):
        trimmed_path = data.removeprefix(PATH_PREFIX).removesuffix(PATH_SUFFIX).strip()
        return read_file(trimmed_path)

    elif isinstance(data, (list, tuple, set, frozenset)):
        return [load_segregated_configs(item) for item in data]

    if isinstance(data, dict):
        return {key: load_segregated_configs(value) for key, value in data.items()}

    return data


def load_base_config(data: Dict[Hashable, Any]) -> Dict[Hashable, Any]:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = load_base_config(value)

    base_data = data.pop(BASE_CONFIG_KEY, None)

    if base_data is not None:
        data = update_nested_dict(base_data, data)

    return data


def load_config(path_to_file: Union[str, PathLike[str], Path]) -> Dict[Hashable, Any]:
    data: Dict[str, Any] = read_file(path_to_file)
    data = load_segregated_configs(data)
    data = load_base_config(data)

    return data

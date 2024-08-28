from os import PathLike
from pathlib import Path
from typing import Any, Dict, Hashable, List, TypedDict, Union

from .readers import read_file

__all__ = [
    "PATH_PREFIX",
    "PATH_SUFFIX",
    "BASE_CONFIG_KEY",
    "SEGREGATE_OPTIONS_KEY",
    "SegregateOptions",
    "load_config",
    "load_segregated_configs",
    "load_base_config",
]


PATH_PREFIX = r"${{"
"""Prefix used to identify a file path that needs to be loaded."""
PATH_SUFFIX = r"}}"
"""Suffix used to identify the end of a file path that needs to be loaded."""
BASE_CONFIG_KEY = r"__base__"
"""Key in the configuration dictionary that represents the base configuration,
which will be updated with other nested configurations."""
SEGREGATE_OPTIONS_KEY = r"__segregate_options__"
"""Key in the configuration dictionary that specifies options for segregating
or updating the nested configuration data."""


class SegregateOptions(TypedDict):
    disable_nested_update: bool
    """Flag to disable nested updates for this configuration."""
    remove_keys: List[Hashable]
    """List of keys to be removed from the configuration during the update process."""


def update_nested_dict(data: Dict[Hashable, Any], updates: Any) -> Any:
    """
    Recursively updates a nested dictionary with new values.

    Args:
        data (Dict[Hashable, Any]): The original dictionary to be updated.
        updates (Any): The updates to apply, which can be a dictionary or another value.

    Returns:
        Dict[Hashable, Any]: The updated dictionary.
    """
    if not isinstance(updates, dict):
        return updates

    segregate_options: SegregateOptions = updates.pop(SEGREGATE_OPTIONS_KEY, {})

    for key_to_remove in segregate_options.get("remove_keys", []):
        data.pop(key_to_remove, None)

    if segregate_options.get("disable_nested_update", False):
        return updates

    for key, value in updates.items():
        current_value = data.get(key)

        if isinstance(current_value, dict):
            data[key] = update_nested_dict(current_value, value)
        else:
            data[key] = value

    return data


def load_segregated_configs(data: Any) -> Any:
    """
    Recursively loads and processes configuration data that may contain file paths or nested structures.

    Args:
        data (Any): The configuration data to be processed. It can be a string, dictionary, or a collection.

    Returns:
        Any: The processed configuration data, with file paths loaded and nested structures updated.
    """
    if isinstance(data, str) and data.startswith(PATH_PREFIX) and data.endswith(PATH_SUFFIX):
        data = data[len(PATH_PREFIX) :]
        data = data[: -len(PATH_SUFFIX)]
        trimmed_path = data.strip()
        data = read_file(trimmed_path)

    if isinstance(data, dict):
        return {key: load_segregated_configs(value) for key, value in data.items()}

    elif isinstance(data, (list, tuple, set, frozenset)):
        return [load_segregated_configs(item) for item in data]

    return data


def load_base_config(data: Dict[Hashable, Any]) -> Dict[Hashable, Any]:
    """
    Processes a configuration dictionary by applying the base configuration specified under `BASE_CONFIG_KEY`.

    Args:
        data (Dict[Hashable, Any]): The configuration dictionary to be processed.

    Returns:
        Dict[Hashable, Any]: The processed configuration dictionary with the base configuration applied.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = load_base_config(value)

    base_data = data.pop(BASE_CONFIG_KEY, None)

    if base_data is not None:
        data = update_nested_dict(base_data, data)

    return data


def load_config(path_to_file: Union[str, PathLike[str], Path]) -> Dict[Hashable, Any]:
    """
    Loads and processes a configuration file.

    Args:
        path_to_file (Union[str, PathLike[str], Path]): The path to the configuration file.

    Returns:
        Dict[Hashable, Any]: The processed configuration dictionary.
    """
    data: Dict[Hashable, Any] = read_file(path_to_file)
    data = load_segregated_configs(data)
    data = load_base_config(data)

    return data

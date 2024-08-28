import json
from os import PathLike
from pathlib import Path
from typing import Any, Callable, Dict, Hashable, Union

import yaml

try:
    import toml
except ImportError:
    WITH_TOML = False
else:
    WITH_TOML = True


__all__ = [
    "ReaderFunc",
    "register_reader",
    "read_file",
]


ReaderFunc = Callable[[Path], Dict[Hashable, Any]]
"""A type alias for reader functions, which take a `Path` and return a dictionary of parsed data."""


READER_REGISTRY: Dict[str, ReaderFunc] = dict()
"""A registry mapping file extensions to their corresponding reader functions."""


def register_reader(key: str, reader_func: ReaderFunc) -> None:
    """
    Registers a new reader function for a specific file extension.

    Args:
        key (str): The file extension (including the leading dot) to associate with the reader function.
        reader_func (ReaderFunc): The function that will handle reading and parsing files with the specified extension.
    """
    READER_REGISTRY[key] = reader_func


def read_file(path_to_file: Union[str, PathLike[str], Path]) -> Dict[Hashable, Any]:
    """
    Reads and parses a file based on its extension using the appropriate reader function.

    Args:
        path_to_file (Union[str, PathLike[str], Path]): The path to the file to be read.

    Returns:
        Dict[Hashable, Any]: The parsed content of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        OSError: If the specified path is not a file.
        ValueError: If no reader function is registered for the file's extension.
    """
    if not isinstance(path_to_file, Path):
        path_to_file = Path(path_to_file)

    if not path_to_file.exists():
        raise FileNotFoundError(f"File `{path_to_file}` was not found.")

    if not path_to_file.is_file():
        raise OSError(f"`{path_to_file}` should be a file.")

    file_extension = path_to_file.suffix

    if file_extension not in READER_REGISTRY:
        raise ValueError(
            f"Does not support `{file_extension}` extension. "
            "Consider implementing your own implementation and "
            "registering using `register_reader` function."
        )

    return READER_REGISTRY[file_extension](path_to_file)


def read_json_file(path_to_file: Path) -> Dict[Hashable, Any]:
    with open(path_to_file) as json_file:
        data: Dict[Hashable, Any] = json.load(json_file)

    return data


def read_yaml_file(path_to_file: Path) -> Dict[Hashable, Any]:
    with open(path_to_file) as yaml_file:
        data: Dict[Hashable, Any] = yaml.safe_load(yaml_file)

    return data


def read_toml_file(path_to_file: Path) -> Dict[Hashable, Any]:
    if not WITH_TOML:
        raise ModuleNotFoundError("Library `toml` is required to directly work with toml files.")

    with open(path_to_file) as toml_file:
        data: Dict[Hashable, Any] = toml.load(toml_file)  # type: ignore

    return data


# Registering default readers for common file extensions
register_reader(".json", read_json_file)
register_reader(".yml", read_yaml_file)
register_reader(".yaml", read_yaml_file)
register_reader(".toml", read_toml_file)

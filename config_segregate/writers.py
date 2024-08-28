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
    "WriterFunc",
    "register_writer",
    "write_file",
]


WriterFunc = Callable[[Path, Dict[Hashable, Any]], None]
"""A type alias for writer functions, which take a `Path` and a dictionary of data to write to the file."""

WRITER_REGISTRY: Dict[str, WriterFunc] = dict()
"""A registry mapping file extensions to their corresponding writer functions."""


def register_writer(key: str, writer_func: WriterFunc) -> None:
    """
    Registers a new writer function for a specific file extension.

    Args:
        key (str): The file extension (including the leading dot) to associate with the writer function.
        writer_func (WriterFunc): The function that will handle writing data to files with the specified extension.
    """
    WRITER_REGISTRY[key] = writer_func


def write_file(path_to_file: Union[str, PathLike[str], Path], data: Dict[Hashable, Any]) -> None:
    """
    Writes data to a file based on its extension using the appropriate writer function.

    Args:
        path_to_file (Union[str, PathLike[str], Path]): The path to the file where data will be written.
        data (Dict[str, Any]): The data to write to the file.

    Raises:
        OSError: If the parent directory does not exist.
        FileExistsError: If the file already exists.
        ValueError: If no writer function is registered for the file's extension.
    """
    if not isinstance(path_to_file, Path):
        path_to_file = Path(path_to_file)

    if not path_to_file.parent.exists():
        raise OSError("Missing folder.")

    if path_to_file.exists():
        raise FileExistsError(f"File `{path_to_file}` already exist.")

    file_extension = path_to_file.suffix

    if file_extension not in WRITER_REGISTRY:
        raise ValueError(
            f"Does not support `{file_extension}` extension. "
            "Consider implementing your own implementation and "
            "registering using `register_writer` function."
        )

    return WRITER_REGISTRY[file_extension](path_to_file, data)


def write_json_file(path_to_file: Path, data: Dict[Hashable, Any]) -> None:
    with open(path_to_file, "w") as json_file:
        json.dump(data, json_file)


def write_yaml_file(path_to_file: Path, data: Dict[Hashable, Any]) -> None:
    with open(path_to_file, "w") as yaml_file:
        yaml.dump(data, yaml_file)


def write_toml_file(path_to_file: Path, data: Dict[Hashable, Any]) -> None:
    if not WITH_TOML:
        raise ModuleNotFoundError("Library `toml` is required to directly work with toml files.")

    with open(path_to_file, "w") as toml_file:
        toml.dump(data, toml_file)  # type: ignore


# Registering default writers for common file extensions
register_writer(".json", write_json_file)
register_writer(".yml", write_yaml_file)
register_writer(".yaml", write_yaml_file)
register_writer(".toml", write_toml_file)

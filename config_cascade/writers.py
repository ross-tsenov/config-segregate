import json
from os import PathLike
from pathlib import Path
from typing import Any, Callable, Dict, Union

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


WriterFunc = Callable[[Path, Dict[str, Any]], None]

WRITER_REGISTRY: Dict[str, WriterFunc] = dict()


def register_writer(key: str, writer_func: WriterFunc) -> None:
    WRITER_REGISTRY[key] = writer_func


def write_file(path_to_file: Union[str, PathLike[str], Path], data: Dict[str, Any]) -> None:
    if not isinstance(path_to_file, Path):
        path_to_file = Path(path_to_file)

    if not path_to_file.parent.exists():
        raise IOError("Missing folder.")

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


def write_json_file(path_to_file: Path, data: Dict[str, Any]) -> None:
    with open(path_to_file, "w") as json_file:
        json.dump(data, json_file)


def write_yaml_file(path_to_file: Path, data: Dict[str, Any]) -> None:
    with open(path_to_file, "w") as yaml_file:
        yaml.dump(data, yaml_file)


def write_toml_file(path_to_file: Path, data: Dict[str, Any]) -> None:
    if not WITH_TOML:
        raise ModuleNotFoundError("Library `toml` is required to directly work with toml files.")

    with open(path_to_file, "w") as toml_file:
        toml.dump(data, toml_file)


register_writer(".json", write_json_file)
register_writer(".yml", write_yaml_file)
register_writer(".yaml", write_yaml_file)
register_writer(".toml", write_toml_file)

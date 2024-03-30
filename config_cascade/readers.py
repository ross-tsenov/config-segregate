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


ReaderFunc = Callable[[Path], Dict[str, Any]]

READER_REGISTRY: Dict[str, ReaderFunc] = dict()


def register_reader(key: str, reader_func: ReaderFunc) -> None:
    READER_REGISTRY[key] = reader_func


def read_file(path_to_file: Union[str, PathLike[str], Path]) -> Dict[str, Any]:
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


def read_json_file(path_to_file: Path) -> Dict[str, Any]:
    with open(path_to_file) as json_file:
        data = json.load(json_file)

    return data


def read_yaml_file(path_to_file: Path) -> Dict[str, Any]:
    with open(path_to_file) as yaml_file:
        data = yaml.safe_load(yaml_file)

    return data


def read_toml_file(path_to_file: Path) -> Dict[str, Any]:
    if not WITH_TOML:
        raise ModuleNotFoundError("Library `toml` is required to directly to work with toml files.")

    with open(path_to_file) as toml_file:
        data = toml.load(toml_file)

    return data


register_reader(".json", read_json_file)
register_reader(".yml", read_yaml_file)
register_reader(".yaml", read_yaml_file)
register_reader(".toml", read_toml_file)

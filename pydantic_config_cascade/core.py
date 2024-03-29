from pydantic import BaseModel, model_validator
from typing import Any, Optional, Union
from pathlib import Path
from os import PathLike
from .readers import read_file


PATH_PREFIX = r"${{"
PATH_SUFFIX = r"}}"
BASE_CONFIG_KEY = r"__base__"


# TODO add setting to do weird nested dict update or not (replace entire dict or partial).

class BaseCascadeModel(BaseModel):

    def __init__(self, path_to_file: Optional[Union[str, PathLike[str], Path]] = None, /, **data) -> None:
        if path_to_file is not None:
            data = read_file(path_to_file)

        super().__init__(**data)

    @model_validator(mode="before")
    @classmethod
    def check_for_base_config(cls, data: dict[str, Any]) -> Any:
        if BASE_CONFIG_KEY not in data:
            return data

        base_data = read_file(data[BASE_CONFIG_KEY])
        base_data.update(data)

        return base_data

    @model_validator(mode="before")
    @classmethod
    def check_for_cascaded_configs(cls, data: dict[str, Any]) -> Any:
        for key, value in data.items():
            if isinstance(value, str) and value.startswith(PATH_PREFIX) and value.endswith(PATH_SUFFIX):
                trimmed_path = value.removeprefix(PATH_PREFIX).removesuffix(PATH_SUFFIX).strip()
                cascaded_data = read_file(trimmed_path)
                data[key] = cascaded_data

        return data

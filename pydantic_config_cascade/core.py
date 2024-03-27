from pydantic import BaseModel, model_validator
from typing import Any
from pathlib import Path


PATH_PREFIX = r"{{"
PATH_SUFFIX = r"}}"


class BaseCascadeModel(BaseModel):

    @model_validator(mode='before')
    @classmethod
    def check_card_number_omitted(cls, data: dict[str, Any]) -> Any:
        if not isinstance(data, dict):
            raise ValueError("Input should be dict.")

        for key, value in data.items():
            if isinstance(value, str) and value.startswith(PATH_PREFIX) and value.endswith(PATH_SUFFIX):
                trimmed_path = value.removeprefix(PATH_PREFIX).removesuffix(PATH_SUFFIX)
                # Clean path
                # Check what type is the file use correct data loader
                # Make registry for loaders based on the file extensions
                # Add functions to register new file extensions readers
                # Start just with jSON though.
                # load file replace string with dict.

        return data


class Some(BaseCascadeModel):
    some: int
    some_2: str


class SomeBlah(BaseCascadeModel):
    some: str
    some_blah: Some


test = SomeBlah("sad", Some(10, "sad"))

from typing import Any, Dict

import pytest

from config_segregate import load_config


def test_loading_and_parsing_of_json_configs(json_configs: Dict[str, Any]) -> None:
    for path_to_file, expected_config in json_configs.items():
        loaded_config = load_config(path_to_file)

        assert loaded_config == expected_config


def test_loading_and_parsing_of_yaml_configs(yaml_configs: Dict[str, Any]) -> None:
    for path_to_file, expected_config in yaml_configs.items():
        loaded_config = load_config(path_to_file)

        assert loaded_config == expected_config


def test_loading_and_parsing_of_yml_configs(yml_configs: Dict[str, Any]) -> None:
    for path_to_file, expected_config in yml_configs.items():
        loaded_config = load_config(path_to_file)

        assert loaded_config == expected_config


def test_loading_and_parsing_of_toml_configs(toml_configs: Dict[str, Any]) -> None:
    for path_to_file, expected_config in toml_configs.items():
        loaded_config = load_config(path_to_file)

        assert loaded_config == expected_config


@pytest.mark.parametrize("execution_number", range(5))
def test_loading_and_parsing_of_random_configs(random_configs: Dict[str, Any], execution_number: int) -> None:
    for path_to_file, expected_config in random_configs.items():
        loaded_config = load_config(path_to_file)

        assert loaded_config == expected_config


# TODO try test for unexisting path, wrong file format, registering file reader/ writer,

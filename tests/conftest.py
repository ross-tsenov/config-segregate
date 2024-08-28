import random
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Hashable, Literal

import pytest

from config_segregate import write_file

SUPPORTED_FILE_FORMATS = ["json", "yaml", "yml", "toml"]
SupportedFileFormats = Literal["json", "yaml", "yml", "toml", "random"]
RANDOM_SEED = 101

random.seed(RANDOM_SEED)


SEGREGATED_CONFIGS = {
    "{tmp_path}/base.{ext}": {
        "name": "BaseConfig",
        "settings": {"language": "English", "timezone": "UTC"},
        "services": {"database": "enabled", "cache": "disabled"},
    },
    "{tmp_path}/link_1.{ext}": {
        "name": "LinkConfig1",
        "features": {"authentication": "oauth2", "logging": "verbose"},
    },
    "{tmp_path}/link_2.{ext}": {
        "name": "LinkConfig2",
        "parameters": {"retry": 3, "timeout": 5000},
    },
    "{tmp_path}/derived_1.{ext}": {
        "__base__": "${{ {tmp_path}/base.{ext} }}",
        "name": "DerivedConfig1",
        "settings": {"timezone": "EST"},
        "services": {"cache": "enabled"},
        "additional": "${{ {tmp_path}/link_1.{ext} }}",
        "further": "${{ {tmp_path}/link_2.{ext} }}",
    },
    "{tmp_path}/link_3.{ext}": {
        "name": "LinkConfig3",
        "data": {"priority": "high", "mode": "active"},
    },
    "{tmp_path}/link_4.{ext}": {
        "__base__": "${{ {tmp_path}/link_3.{ext} }}",
        "name": "LinkConfig4",
        "data": {
            "priority": "low",
        },
    },
    "{tmp_path}/derived_2.{ext}": {
        "__base__": "${{ {tmp_path}/derived_1.{ext} }}",
        "name": "DerivedConfig2",
        "settings": {"language": "Spanish"},
        "additional_links": {
            "third": "${{ {tmp_path}/link_3.{ext} }}",
            "fourth": "${{ {tmp_path}/link_4.{ext} }}",
        },
    },
    "{tmp_path}/secrets_base.{ext}": {
        "name": "SecretsBase",
        "key": "secret_key_base",
        "password": "secret_password_base",
    },
    "{tmp_path}/backup_secrets.{ext}": {
        "__base__": "${{ {tmp_path}/secrets_base.{ext} }}",
        "name": "BackupSecrets",
        "password": "secret_password_base",
    },
    "{tmp_path}/external_link.{ext}": {
        "name": "ExternalLinkConfig",
        "parameters": {"timeout": 5000, "retry": 3},
    },
    "{tmp_path}/internal_link.{ext}": {
        "name": "InternalLinkConfig",
        "data": {"priority": "high", "mode": "active"},
    },
    "{tmp_path}/backup_link.{ext}": {
        "__base__": "${{ {tmp_path}/internal_link.{ext} }}",
        "name": "BackupLinkConfig",
        "data": {"priority": "low"},
        "secrets": "${{ {tmp_path}/backup_secrets.{ext} }}",
    },
    "{tmp_path}/derived_3.{ext}": {
        "__base__": "${{ {tmp_path}/base.{ext} }}",
        "name": "DerivedConfig3",
        "settings": {"language": "French"},
        "services": {"cache": "Memcached"},
        "links": {
            "external": "${{ {tmp_path}/external_link.{ext} }}",
            "internal_link": "${{ {tmp_path}/internal_link.{ext} }}",
            "backup_link": "${{ {tmp_path}/backup_link.{ext} }}",
        },
    },
}


EXPECTED_CONFIGS = {
    "{tmp_path}/base.{ext}": {
        "name": "BaseConfig",
        "settings": {
            "language": "English",
            "timezone": "UTC",
        },
        "services": {
            "database": "enabled",
            "cache": "disabled",
        },
    },
    "{tmp_path}/derived_1.{ext}": {
        "name": "DerivedConfig1",
        "settings": {
            "language": "English",
            "timezone": "EST",
        },
        "services": {
            "database": "enabled",
            "cache": "enabled",
        },
        "additional": {
            "name": "LinkConfig1",
            "features": {
                "authentication": "oauth2",
                "logging": "verbose",
            },
        },
        "further": {
            "name": "LinkConfig2",
            "parameters": {
                "retry": 3,
                "timeout": 5000,
            },
        },
    },
    "{tmp_path}/derived_2.{ext}": {
        "name": "DerivedConfig2",
        "settings": {
            "language": "Spanish",
            "timezone": "EST",
        },
        "services": {
            "database": "enabled",
            "cache": "enabled",
        },
        "additional": {
            "name": "LinkConfig1",
            "features": {
                "authentication": "oauth2",
                "logging": "verbose",
            },
        },
        "further": {
            "name": "LinkConfig2",
            "parameters": {
                "retry": 3,
                "timeout": 5000,
            },
        },
        "additional_links": {
            "third": {
                "name": "LinkConfig3",
                "data": {
                    "priority": "high",
                    "mode": "active",
                },
            },
            "fourth": {
                "name": "LinkConfig4",
                "data": {
                    "priority": "low",
                    "mode": "active",
                },
            },
        },
    },
    "{tmp_path}/derived_3.{ext}": {
        "name": "DerivedConfig3",
        "settings": {
            "language": "French",
            "timezone": "UTC",
        },
        "services": {
            "database": "enabled",
            "cache": "Memcached",
        },
        "links": {
            "external": {
                "name": "ExternalLinkConfig",
                "parameters": {"timeout": 5000, "retry": 3},
            },
            "internal_link": {
                "name": "InternalLinkConfig",
                "data": {"priority": "high", "mode": "active"},
            },
            "backup_link": {
                "name": "BackupLinkConfig",
                "data": {
                    "priority": "low",
                    "mode": "active",
                },
                "secrets": {
                    "name": "BackupSecrets",
                    "key": "secret_key_base",
                    "password": "secret_password_base",
                },
            },
        },
    },
}


def format_segregated_configs(configs: Dict[Hashable, Any], old_file_key: str, new_file_key: str) -> None:
    def format_nested_path(config: Dict[Hashable, Any]) -> None:
        for key, value in config.items():
            if isinstance(value, dict):
                format_nested_path(value)

            if not isinstance(value, str):
                continue

            if old_file_key not in value:
                continue

            config[key] = value.replace(old_file_key, new_file_key)

    format_nested_path(configs)


def format_configs(
    segregated_configs: Dict[Hashable, Any],
    expected_configs: Dict[Hashable, Any],
    tmp_dir: Path,
    file_ext: SupportedFileFormats = "json",
) -> None:
    for old_file_key in list(segregated_configs.keys())[:]:
        extension = file_ext if file_ext != "random" else random.choice(SUPPORTED_FILE_FORMATS)  # type: ignore
        new_file_key = old_file_key.format(tmp_path=tmp_dir, ext=extension)
        segregated_configs[new_file_key] = segregated_configs.pop(old_file_key)

        if old_file_key in expected_configs:
            expected_configs[new_file_key] = expected_configs.pop(old_file_key)

        format_segregated_configs(segregated_configs, old_file_key, new_file_key)


def save_configs(configs: Dict[Hashable, Any]) -> None:
    for path_to_config, data in configs.items():
        write_file(Path(path_to_config), data)


def prepare_configs(
    segregated_configs: Dict[Hashable, Any],
    expected_configs: Dict[Hashable, Any],
    tmp_dir: Path,
    file_ext: SupportedFileFormats = "json",
) -> None:
    format_configs(segregated_configs, expected_configs, tmp_dir, file_ext)
    if not tmp_dir.exists():
        tmp_dir.mkdir()
    save_configs(segregated_configs)


@pytest.fixture()
def json_configs(tmp_path: Path) -> Dict[Hashable, Any]:
    segregated_configs = deepcopy(SEGREGATED_CONFIGS)
    expected_configs = deepcopy(EXPECTED_CONFIGS)

    prepare_configs(segregated_configs, expected_configs, tmp_path, "json")
    return expected_configs


@pytest.fixture()
def yaml_configs(tmp_path: Path) -> Dict[Hashable, Any]:
    segregated_configs = deepcopy(SEGREGATED_CONFIGS)
    expected_configs = deepcopy(EXPECTED_CONFIGS)

    prepare_configs(segregated_configs, expected_configs, tmp_path, "yaml")
    return expected_configs


@pytest.fixture()
def yml_configs(tmp_path: Path) -> Dict[Hashable, Any]:
    segregated_configs = deepcopy(SEGREGATED_CONFIGS)
    expected_configs = deepcopy(EXPECTED_CONFIGS)

    prepare_configs(segregated_configs, expected_configs, tmp_path, "yml")
    return expected_configs


@pytest.fixture()
def toml_configs(tmp_path: Path) -> Dict[Hashable, Any]:
    segregated_configs = deepcopy(SEGREGATED_CONFIGS)
    expected_configs = deepcopy(EXPECTED_CONFIGS)

    prepare_configs(segregated_configs, expected_configs, tmp_path, "toml")
    return expected_configs


@pytest.fixture()
def random_configs(tmp_path: Path) -> Dict[Hashable, Any]:
    segregated_configs = deepcopy(SEGREGATED_CONFIGS)
    expected_configs = deepcopy(EXPECTED_CONFIGS)

    prepare_configs(segregated_configs, expected_configs, tmp_path, "random")
    return expected_configs

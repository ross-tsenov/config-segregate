---

[![Build Status](https://github.com/ross-tsenov/config-segregate/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ross-tsenov/config-segregate/actions/workflows/ci.yml)
[![PyPI Version](https://badge.fury.io/py/config-segregate.svg)](https://pypi.python.org/pypi/config-segregate)
[![Supported Python Version](https://img.shields.io/pypi/pyversions/config-segregate.svg?color=%2334D058)](https://pypi.python.org/pypi/config-segregate)
---
### **[Documentation](https://ross-tsenov.github.io/config-segregate/)**

---

# Config-Segregate

Config-Segregate is a Python library that simplifies the management of complex configuration files. It allows you to split configurations into multiple files, use different formats (JSON, YAML, TOML), and apply updates to a base configuration, reducing redundancy and making it easier to manage large configurations. Also, it works well with [Pydantic](https://pypi.org/project/pydantic/).

## Features

- **Modular Configurations**: Split your configuration into multiple files, each in a different format if needed.
- **Base and Updates**: Define a base configuration and apply updates from other files on top of it, supporting nested updates.
- **Support for JSON, YAML, and TOML**: Easily load configurations in multiple formats.
- **Custom Readers**: Extend the library by registering custom reader functions for additional file formats.
- **Segregation Options**: Control how configurations are merged, with options to disable nested updates or remove specific keys.

## Requirements

Python 3.8+

## Installation

```shell
$ pip3 install config-segregate
```


## Usage

### Basic Example

Suppose you have a configuration file `main_config.json` that references a base configuration and another settings file:

```json
{
    "__base__": "${{ base_config.json }}",
    "logging": {
        "level": "DEBUG",
        "settings": "${{ ./settings/settings.json }}"
    }
}
```

You can load this configuration using the `load_config` function:

```python
from config_loader import load_config

config = load_config("path/to/main_config.json")
print(config)
```

This will load the `main_config.json`, resolve the referenced paths, apply updates from the file on top of the base configuration, and return the final merged configuration as a Python dictionary.

### Segregation Options

You can control how configurations are merged using the `__segregate_options__` key:

```json
{
    "__base__": "${{ base_config.json }}",
    "__segregate_options__": {
        "disable_nested_update": true,
        "remove_keys": ["obsolete_key"]
    },
    "logging": {
        "level": "DEBUG"
    }
}
```

### Custom Readers

To add support for custom file formats, register a custom reader function:

```python
from config_loader import register_reader

def read_custom_file(path_to_file):
    with open(path_to_file) as custom_file:
        data = custom_file.read()
        # Process your custom data format here and return as a dictionary
        return process_custom_data(data)

register_reader(".custom", read_custom_file)
```

Now, you can load `.custom` files just like any other supported format:

```python
config = load_config("path/to/config.custom")
```

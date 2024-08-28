---
hide:
  - navigation
---

# Config-Segregate

The `config-segregate` library is designed to help you manage and load configuration files that are split into multiple files, potentially using different formats (e.g., JSON, YAML, TOML). This modular approach allows you to separate different parts of your configuration into their own files. The library also provides the ability to define a "Base" configuration and apply "Updates" on top of it, reducing duplication and simplifying configuration management. Also, it works well with [Pydantic](https://pypi.org/project/pydantic/).

## Key Features:

- **Modular Configurations**: Configurations can be split across multiple files, each of which can be in a different format, as long as they can be loaded as Python dictionaries.
- **Base and Updates**: You can define a base configuration and apply updates from other files on top of it. This approach supports nested updates, meaning that if the base contains nested dictionaries, the updates will not replace them entirely but will update them recursively.- **Support for JSON, YAML, and TOML**: Easily load configurations in multiple formats.
- **Custom Readers**: Extend the library by registering custom reader functions for additional file formats.
- **Segregation Options**: Control how configurations are merged, with options to disable nested updates or remove specific keys.

## Requirements

Python 3.8+

## Installation

```shell
$ pip3 install config-segregate
```

## Example

Suppose you have a configuration file `main_config.json` that references another file `base_config.json` and also includes settings from `settings.json`:

```json
{
    "__base__": "${{ base_config.json }}",
    "logging": {
        "level": "DEBUG",
        "settings": "${{ ./settings/settings.json }}"
    }
}
```

In this example:
- The `__base__` key references `base_config.json`, whose contents will be loaded and merged with `main_config.json`.
- The `settings` key within the `logging` section references another file, `settings.json`, which will be loaded and included in the final configuration.

You can mix and match file formats (e.g., the base file can be JSON, while the settings file can be YAML) as long as they can be loaded as Python dictionaries.

## Loading the Configuration

To load and resolve any references within your configuration file, use the `load_config` function:

```python
from config_loader import load_config

config = load_config("path/to/main_config.json")
print(config)
```

This function will:
- Load `main_config.json`.
- Resolve any referenced paths.
- Apply updates from the file on top of the base configuration specified in the `__base__` key.
- Return the final merged configuration as a Python dictionary.

## TOML Support

If you need to work with TOML files, you can optionally install the `toml` library by using the `toml` extra:

```sh
$ pip3 install config-segregate[toml]
# or
$ pip3 install config-segregate[all]
```

This will enable support for reading TOML files with the `load_config` function.

## Segregation Options

The `config-segregate` library also provides options to control how configurations are merged. These options can be specified in your configuration files using the `__segregate_options__` key.

### Available Segregation Options

The `SegregateOptions` dictionary includes the following options:

- **`disable_nested_update`**: A boolean flag that, when set to `True`, disables nested updates. Instead of updating nested dictionaries, the update will replace them entirely.
- **`remove_keys`**: A list of keys that should be removed from the configuration during the update process.

### Example Usage in JSON

Here’s how you can specify these options in a JSON configuration file:

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

In this example:
- `disable_nested_update: true` means that any nested dictionaries in the base configuration will be replaced by the corresponding entries in this file.
- `remove_keys: ["obsolete_key"]` indicates that the key `obsolete_key` should be removed from the base configuration during the update.

## Registering Custom Readers

The library is extendable, allowing you to add support for custom file formats by registering your own reader functions.

### Example

Suppose you have a custom configuration format with a `.custom` extension. Here’s how you could add support for it:

```python
from config_loader import register_reader

def read_custom_file(path_to_file):
    with open(path_to_file) as custom_file:
        data = custom_file.read()
        # Process your custom data format here and return as a dictionary
        return process_custom_data(data)

register_reader(".custom", read_custom_file)
```

After registering, you can load `.custom` files just like any other supported format:

```python
config = load_config("path/to/config.custom")
```

### Custom Reader Function Signature

Your custom reader function should follow this signature:

```python
def custom_reader_function(path_to_file: Path) -> Dict[str, Any]:
    # Your code to read and return data as a dictionary
```

This approach allows you to seamlessly extend the library's capabilities to handle any file format your project requires.

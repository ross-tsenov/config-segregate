def get_version_from_pyproject(filename: str) -> str:
    """Loads version from .toml file."""
    with open(filename) as file:
        for line in file:
            if not line.strip().startswith("version"):
                continue
            version = line.split("=")[1].strip().strip('"').strip("'")
            return version

    return ""


__version__ = get_version_from_pyproject("./pyproject.toml")

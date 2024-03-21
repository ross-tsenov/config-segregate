from pathlib import Path

import pytest

from src import get_version_from_pyproject


@pytest.fixture()
def path_to_pyproject(tmp_path: Path) -> Path:
    temp_dir = tmp_path / "sub"
    temp_dir.mkdir()
    file = temp_dir / "pyproject.toml"
    return file


def test_get_version_from_pyproject(path_to_pyproject: Path) -> None:
    version = "1.2.3"
    path_to_pyproject.write_text(f"version = '{version}'")
    result = get_version_from_pyproject(str(path_to_pyproject))
    assert version == result


def test_get_version_from_empty_pyproject(path_to_pyproject: Path) -> None:
    path_to_pyproject.write_text("")
    version = get_version_from_pyproject(str(path_to_pyproject))
    assert version == ""


def test_get_version_from_nonexistent_file() -> None:
    with pytest.raises(FileNotFoundError):
        get_version_from_pyproject("nonexistent_file.toml")

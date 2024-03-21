import os
from unittest.mock import patch

import pytest
from pydantic_core import ValidationError

from src.settings import Environment, Settings


def test_environment_override() -> None:
    """Test overriding settings through environment variables."""
    with patch.dict(os.environ, {"ENV": "prod", "LOGGER_NAME": "test_logger", "LOGGING_LEVEL": "DEBUG"}):
        settings = Settings()
        assert settings.env == Environment.PROD
        assert settings.logger_name == "test_logger"
        assert settings.logging_level == "DEBUG"


def test_invalid_environment() -> None:
    """Test setting an invalid environment variable."""
    with patch.dict(os.environ, {"ENV": "INVALID_ENV"}):
        with pytest.raises(ValidationError):
            Settings()


def test_invalid_logging_level() -> None:
    """Test setting an invalid logging level."""
    with patch.dict(os.environ, {"LOGGING_LEVEL": "INVALID_LEVEL"}):
        with pytest.raises(ValidationError):
            Settings()

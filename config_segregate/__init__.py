from importlib.metadata import PackageNotFoundError, version

from .core import *
from .readers import *
from .writers import *

try:
    __version__ = version("config_segregate")
except PackageNotFoundError:
    __version__ = "0.0.0"

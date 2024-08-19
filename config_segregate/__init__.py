from .core import *
from .readers import *
from .writers import *
from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version("config_segregate")
except PackageNotFoundError:
    __version__ = "0.0.0"

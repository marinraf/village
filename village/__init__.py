from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("village")
except PackageNotFoundError:
    # package is not installed
    pass

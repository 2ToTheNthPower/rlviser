# PyViser - pip-installable version of VirxEC/rlviser
# This package provides pre-built binaries
import sys
from pathlib import Path


def get_binary_path():
    """Get the path to the pyviser binary for the current platform"""
    binary_name = "pyviser.exe" if sys.platform == "win32" else "pyviser"
    return Path(__file__).parent / "bin" / binary_name


# Export the binary path for users who want to access it programmatically
BINARY_PATH = get_binary_path()

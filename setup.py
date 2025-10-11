from setuptools import setup, find_packages
import sys
from pathlib import Path

# Determine which binary to include based on platform
if sys.platform == "win32":
    scripts = []
    data_files = [("Scripts", ["pyviser/bin/pyviser.exe"])]
else:
    scripts = ["pyviser/bin/pyviser"]
    data_files = []

setup(
    packages=find_packages(),
    scripts=scripts,
    data_files=data_files,
)

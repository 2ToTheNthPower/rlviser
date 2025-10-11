#!/usr/bin/env python3
"""Install the pyviser binary to your PATH"""

import sys
import os
import shutil
from pathlib import Path


def main():
    # Get the binary path
    from pyviser import BINARY_PATH

    if not BINARY_PATH.exists():
        print(f"Error: Binary not found at {BINARY_PATH}")
        sys.exit(1)

    # Determine destination
    if sys.platform == "win32":
        dest_dir = Path(sys.prefix) / "Scripts"
    else:
        dest_dir = Path(sys.prefix) / "bin"

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_binary = dest_dir / BINARY_PATH.name

    # Copy binary
    print(f"Installing {BINARY_PATH.name} to {dest_binary}")
    shutil.copy2(BINARY_PATH, dest_binary)

    # Make executable on Unix
    if sys.platform != "win32":
        os.chmod(dest_binary, 0o755)

    print(f"Successfully installed {BINARY_PATH.name}")
    print(f"You can now run 'pyviser' from your command line")


if __name__ == "__main__":
    main()

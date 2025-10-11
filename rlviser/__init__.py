"""RLViser - Rocket League replay visualizer"""

import os
import sys
import platform
import subprocess
from pathlib import Path

__version__ = "0.8.3"


def get_binary_name():
    """Get the platform-specific binary name"""
    if platform.system() == "Windows":
        return "rlviser.exe"
    return "rlviser"


def get_binary_path():
    """Get the path to the rlviser binary"""
    package_dir = Path(__file__).parent
    bin_dir = package_dir / "bin"
    binary_name = get_binary_name()
    binary_path = bin_dir / binary_name
    
    if binary_path.exists():
        return str(binary_path)
    
    # Fallback to searching in PATH
    import shutil
    fallback = shutil.which("rlviser")
    if fallback:
        return fallback
    
    raise FileNotFoundError(
        f"rlviser binary not found. Expected at {binary_path}"
    )


def main():
    """Main entry point for the rlviser command"""
    try:
        binary_path = get_binary_path()
        # Pass through all command line arguments
        result = subprocess.run([binary_path] + sys.argv[1:])
        sys.exit(result.returncode)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)  # Standard exit code for Ctrl+C


if __name__ == "__main__":
    main()
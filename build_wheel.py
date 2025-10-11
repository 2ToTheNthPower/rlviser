#!/usr/bin/env python3
"""Helper script to build platform-specific wheel locally"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


def build_rust_binary():
    """Build the Rust binary for the current platform"""
    system = platform.system()
    machine = platform.machine()
    
    if system == "Linux":
        target = "x86_64-unknown-linux-gnu"
    elif system == "Darwin":
        if machine == "arm64":
            target = "aarch64-apple-darwin"
        else:
            target = "x86_64-apple-darwin"
    elif system == "Windows":
        target = "x86_64-pc-windows-msvc"
    else:
        raise ValueError(f"Unsupported platform: {system}")
    
    print(f"Building Rust binary for {target}...")
    subprocess.check_call([
        "cargo", "build", "--release",
        "--target", target,
        "--no-default-features", "--features", "threaded"
    ])
    
    # Copy the binary to the package directory
    binary_name = "rlviser.exe" if system == "Windows" else "rlviser"
    source = Path("target") / target / "release" / binary_name
    dest_dir = Path("rlviser") / "bin"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / binary_name
    
    print(f"Copying {source} to {dest}")
    shutil.copy2(source, dest)
    
    # Make it executable on Unix
    if system != "Windows":
        os.chmod(dest, 0o755)
    
    return dest


def build_wheel():
    """Build the wheel"""
    # Clean previous builds
    for dir_name in ["build", "dist", "*.egg-info"]:
        for path in Path(".").glob(dir_name):
            if path.is_dir():
                shutil.rmtree(path)
    
    # Build the binary
    binary_path = build_rust_binary()
    print(f"Binary built at: {binary_path}")
    
    # Build the wheel
    print("Building wheel...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "build"])
    subprocess.check_call([sys.executable, "-m", "build", "--wheel", "--skip-dependency-check"])
    
    # List the built wheel
    wheels = list(Path("dist").glob("*.whl"))
    if wheels:
        print(f"\nWheel built successfully: {wheels[0]}")
        print(f"\nTo install locally, run:")
        print(f"  pip install {wheels[0]}")
    else:
        print("Warning: No wheel found in dist/")


if __name__ == "__main__":
    build_wheel()
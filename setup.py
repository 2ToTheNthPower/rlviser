import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from setuptools import setup, Command
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install import install
from wheel.bdist_wheel import bdist_wheel


def get_platform_tag():
    """Get the platform-specific wheel tag"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "linux":
        return "manylinux2014_x86_64" if machine == "x86_64" else f"linux_{machine}"
    elif system == "darwin":
        if machine == "arm64":
            return "macosx_11_0_arm64"
        else:
            return "macosx_10_9_x86_64"
    elif system == "windows":
        return "win_amd64" if machine == "amd64" else "win32"
    else:
        return "any"


class BdistWheelCommand(bdist_wheel):
    """Custom wheel command to set platform-specific tags"""
    
    def finalize_options(self):
        super().finalize_options()
        # Force platform-specific wheel
        self.root_is_pure = False
        
    def get_tag(self):
        python, abi, plat = super().get_tag()
        # Use a more specific platform tag
        plat = get_platform_tag()
        # Support any Python version 3.7+
        python = "py3"
        abi = "none"
        return python, abi, plat


class BuildRustBinary(Command):
    """Custom command to build the Rust binary"""
    description = "Build the Rust binary"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        # Check if we're building from a source distribution or a git repo
        if not Path("Cargo.toml").exists():
            # We're likely installing from PyPI, binary should already be included
            return
            
        # Determine the target based on platform
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
        
        # Build the Rust binary
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


class BuildPyCommand(build_py):
    """Custom build_py command that builds Rust binary first"""
    def run(self):
        self.run_command("build_rust")
        super().run()


class DevelopCommand(develop):
    """Custom develop command that builds Rust binary first"""
    def run(self):
        self.run_command("build_rust")
        super().run()


class InstallCommand(install):
    """Custom install command that ensures Rust binary is built"""
    def run(self):
        self.run_command("build_rust")
        super().run()


# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    cmdclass={
        "bdist_wheel": BdistWheelCommand,
        "build_rust": BuildRustBinary,
        "build_py": BuildPyCommand,
        "develop": DevelopCommand,
        "install": InstallCommand,
    },
)
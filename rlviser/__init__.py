import sys
import subprocess
from pathlib import Path

def main():
    binary = Path(__file__).parent / "bin" / ("rlviser.exe" if sys.platform == "win32" else "rlviser")
    sys.exit(subprocess.run([str(binary)] + sys.argv[1:]).returncode)
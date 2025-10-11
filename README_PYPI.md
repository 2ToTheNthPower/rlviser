# RLViser

RLViser is a high-performance Rocket League replay visualizer written in Rust.

## Installation

You can install RLViser directly from PyPI:

```bash
pip install rlviser
```

This will install the `rlviser` command in your Python environment.

## Usage

After installation, you can run RLViser from the command line:

```bash
rlviser
```

## Features

- High-performance replay visualization
- Cross-platform support (Windows, macOS, Linux)
- Built with Rust for maximum performance

## Requirements

- Python 3.7 or higher
- No additional dependencies required - the package includes a pre-built binary

## Platform Support

Pre-built wheels are available for:
- Windows (x86_64)
- macOS (x86_64 and ARM64)
- Linux (x86_64)

## Development

For development or building from source, you'll need:
- Rust toolchain (1.70+)
- Cargo

To build from source:
```bash
git clone https://github.com/yourusername/rlviser.git
cd rlviser
python build_wheel.py
pip install dist/*.whl
```

## License

MIT License - see LICENSE file for details.
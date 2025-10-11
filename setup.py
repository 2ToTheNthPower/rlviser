from setuptools import setup
from setuptools_rust import Binding, RustBin

setup(
    rust_extensions=[
        RustBin(
            "pyviser",
            binding=Binding.Exec,
            features=["threaded"],
            args=["--no-default-features"],
        )
    ],
)

import sys
import tempfile
from dataclasses import dataclass
from random import choice
from typing import Iterator

from pytest import fixture


@dataclass
class PluginPath:
    file_path: str
    py_path: str


@fixture
def plugin_path() -> Iterator[PluginPath]:
    paths: list[str] = [p for p in sys.path if p.endswith("site-packages")]
    base_path: str = choice(paths)
    with tempfile.TemporaryDirectory(dir=base_path) as package_path:
        with open(f"{package_path}/__init__.py", "w"):
            ...
        with tempfile.NamedTemporaryFile(suffix=".py", dir=package_path) as py_path:
            dir_name: str = package_path.split("/")[-1]
            file_name: str = py_path.name.split("/")[-1].split(".")[0]
            yield PluginPath(file_path=py_path.name, py_path=f"{dir_name}.{file_name}")

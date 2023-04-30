import sys
import tempfile
from importlib import invalidate_caches
from random import choice
from types import ModuleType
from typing import Optional

from sugaru.plugin_loader import load_module, load_plugins


def test_load_plugin_name_as_module() -> None:
    module_name: str = "sugaru"
    module: Optional[ModuleType] = load_module(module_name)
    assert module
    assert module.__name__ == module_name


def test_load_module_with_class_specified() -> None:
    module_name: str = "sugaru"
    plugin_name: str = f"{module_name}.Plugin"
    module: Optional[ModuleType] = load_module(plugin_name)

    assert module
    assert module.__name__ == module_name


def test_load_single_plugin() -> None:
    plugin_name: str = "MyAwesomePlugin"
    plugin_content: str = f"""
from sugaru import Section
class {plugin_name}:
    @staticmethod
    def __call__(*, section: Section, section_name: str) -> Section:
        return {{}}
    """

    paths: list[str] = [p for p in sys.path if p.endswith("site-packages")]
    base_path: str = choice(paths)
    with tempfile.TemporaryDirectory(dir=base_path) as package_path:
        with open(f"{package_path}/__init__.py", "w"):
            ...
        with tempfile.NamedTemporaryFile(suffix=".py", dir=package_path) as py_path:
            with open(py_path.name, "w") as f:
                f.write(plugin_content)

            print(f"{package_path = }, {py_path.name = }")
            dir_name: str = package_path.split("/")[-1]
            file_name: str = py_path.name.split("/")[-1].split(".")[0]
            plugin_to_load: str = f"{dir_name}.{file_name}.{plugin_name}"

            invalidate_caches()
            module = load_module(plugin_to_load)
            assert module
            plugin_classes = load_plugins(module, plugin_name=plugin_to_load)

            assert len(plugin_classes) == 1
            assert plugin_classes[0].__name__ == plugin_name


def test_load_all_plugins_in_module() -> None:
    ...

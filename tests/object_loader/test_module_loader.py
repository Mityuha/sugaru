from types import ModuleType
from typing import Optional

from sugaru import load_module


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

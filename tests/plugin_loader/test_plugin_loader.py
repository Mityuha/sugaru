from types import ModuleType
from typing import Optional

from sugaru.plugin_loader import load_module, load_plugins
from . import PluginPath


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


def test_load_single_plugin(plugin_path: PluginPath) -> None:
    plugin_name: str = "MyAwesomePlugin"
    plugin_content: str = f"""
from sugaru import Section
class {plugin_name}:
    @staticmethod
    def __call__(*, section: Section, section_name: str) -> Section:
        return {{}}

class {plugin_name}2:
    @staticmethod
    def __call__(*, section: Section, section_name: str) -> Section:
        return None

def some_custom_function(x: int) -> None:
    print(x)
    """

    with open(plugin_path.file_path, "w") as f:
        f.write(plugin_content)

    plugin_to_load: str = f"{plugin_path.py_path}.{plugin_name}"

    module = load_module(plugin_to_load)
    assert module
    plugin_classes = load_plugins(module, plugin_name=plugin_to_load)

    assert len(plugin_classes) == 1
    assert plugin_classes[0].__name__ == plugin_name


def test_load_all_plugins_in_module(plugin_path: PluginPath) -> None:
    plugin_num: int = 5
    plugin_name: str = "MultiPluginTest"
    plugin_content: str = "\n\n".join(
        f"""
from sugaru import Section
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, section: Section, section_name: str) -> Section:
        return {{}}

def {plugin_name.lower()}{i}(*, section: Section, section_name: str) -> Section:
    return {{}}

def some_custom_func{i}(x: int) -> int:
    return x
    """
        for i in range(plugin_num)
    )

    with open(plugin_path.file_path, "w") as f:
        f.write(plugin_content)

    plugin_to_load: str = f"{plugin_path.py_path}"

    module = load_module(plugin_to_load)
    assert module
    plugin_classes = load_plugins(module, plugin_name=plugin_to_load)

    assert len(plugin_classes) == plugin_num * 2
    assert [p.__name__ for p in plugin_classes] == [
        f"{plugin_name}{i}" for i in range(plugin_num)
    ] + [f"{plugin_name.lower()}{i}" for i in range(plugin_num)]

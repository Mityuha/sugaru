from random import choice
from typing import Any, List, Type

from sugaru import Plugin, load_module, load_objects
from . import PluginContent, PluginPath


def test_load_single_object(plugin_path: PluginPath, plugin_content: PluginContent) -> None:
    plugin_name: str = choice(plugin_content.plugin_names)

    plugin_to_load: str = f"{plugin_path.py_path}.{plugin_name}"

    module = load_module(plugin_to_load)
    assert module
    plugin_classes: List[Type[Plugin]] = load_objects(module, obj_name=plugin_to_load)

    assert len(plugin_classes) == 1
    assert plugin_classes[0].__name__ == plugin_name


def test_load_all_objects_in_module(
    plugin_path: PluginPath, plugin_content: PluginContent
) -> None:
    plugin_to_load: str = plugin_path.py_path

    module = load_module(plugin_to_load)
    assert module
    object_classes: List[Any] = load_objects(module, obj_name=plugin_to_load)

    assert {p.__name__ for p in object_classes} == set(plugin_content.object_names)


def test_load_unknown_object(plugin_path: PluginPath, faker: Any) -> None:
    module = load_module(plugin_path.py_path)
    assert module

    empty_objects: List[Any] = load_objects(
        module, obj_name=f"{plugin_path.py_path}{faker.pystr()}"
    )
    assert empty_objects == []

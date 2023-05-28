from typing import Any, List

from sugaru import Plugin, check_callable_signature, load_module, load_objects
from . import PluginContent, PluginPath


def test_check_all_objects_signatures(
    plugin_path: PluginPath, plugin_content: PluginContent
) -> None:
    module = load_module(plugin_path.py_path)
    assert module
    object_classes: List[Any] = load_objects(module, obj_name=plugin_path.py_path)

    assert len(object_classes) >= len(plugin_content.object_names)

    plugin_classes = [
        object_class
        for object_class in object_classes
        if check_callable_signature(
            object_class,
            class_=Plugin,
            type_check=True,
        )
    ]

    assert set(p.__name__ for p in plugin_classes) == set(plugin_content.plugin_names)


def test_bad_object_signatures(plugin_path: PluginPath, plugin_content: PluginContent) -> None:
    module = load_module(plugin_path.py_path)
    assert module

    object_classes: List[Any] = load_objects(module, obj_name=plugin_path.py_path)
    not_plugins = [
        obj for obj in object_classes if obj.__name__ not in plugin_content.plugin_names
    ]

    plugin_classes = [
        object_class
        for object_class in not_plugins
        if check_callable_signature(
            object_class,
            class_=Plugin,
            type_check=True,
        )
    ]
    assert plugin_classes == []

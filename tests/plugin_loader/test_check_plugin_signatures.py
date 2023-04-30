from sugaru.plugin_loader import check_plugins_signatures, load_module, load_objects
from . import PluginContent, PluginPath


def test_check_all_objects_signatures(
    plugin_path: PluginPath, plugin_content: PluginContent
) -> None:
    module = load_module(plugin_path.py_path)
    assert module
    object_classes = load_objects(module, plugin_name=plugin_path.py_path)

    assert len(object_classes) == len(plugin_content.object_names)

    plugin_classes = check_plugins_signatures(object_classes)

    assert set(p.__name__ for p in plugin_classes) == set(plugin_content.plugin_names)


def test_bad_object_signatures(plugin_path: PluginPath, plugin_content: PluginContent) -> None:
    module = load_module(plugin_path.py_path)
    assert module

    object_classes = load_objects(module, plugin_name=plugin_path.py_path)
    not_plugins = [
        obj for obj in object_classes if obj.__name__ not in plugin_content.plugin_names
    ]

    plugin_classes = check_plugins_signatures(not_plugins)
    assert plugin_classes == []

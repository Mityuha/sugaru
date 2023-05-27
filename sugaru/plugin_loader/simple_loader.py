from inspect import isfunction
from types import ModuleType
from typing import List, Optional, Type

from ..interfaces import Plugin
from ..logging import logger
from .module_loader import load_module
from .object_creator import create_object
from .objects_loader import load_objects
from .signature_checker import check_plugins_signatures


class SimplePluginLoader:
    def __call__(self, plugin_name: str) -> List[Plugin]:
        module: Optional[ModuleType] = load_module(plugin_name)
        if not module:
            logger.info(f"Cannot load module by plugin name '{plugin_name}'")
            return []

        object_classes: List[Type[Plugin]] = load_objects(module, plugin_name=plugin_name)

        logger.trace(
            f"Objects loaded by plugin name '{plugin_name}': {[obj.__name__ for obj in object_classes]}"
        )

        plugin_classes: List[Type[Plugin]] = check_plugins_signatures(object_classes)

        logger.debug(
            f"Plugin '{plugin_name}' classes after signature check: {[p.__name__ for p in plugin_classes]}"
        )

        plugin_objects: List[Plugin] = []
        for plugin_class in plugin_classes:
            obj: Optional[Plugin] = create_object(plugin_class)
            if not obj:
                logger.info(
                    f"Plugin '{plugin_class.__name__}' can't be created in a simple way. Skip."
                )
                continue
            plugin_objects.append(obj)

        def plug_name(obj):
            return obj.__name__ if isfunction(obj) else type(obj).__name__

        logger.debug(
            f"Plugin '{plugin_name}' objects after plugin class instantiating: {[plug_name(p) for p in plugin_objects]}"
        )

        return plugin_objects

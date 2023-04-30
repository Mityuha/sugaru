from importlib import import_module
from types import ModuleType
from typing import List, Optional, Type

from .interfaces import Plugin
from .logging import logger


def load_module(plugin_name: str) -> Optional[ModuleType]:
    module_name: str = plugin_name
    while True:
        logger.trace(f"Try to import module by name '{module_name}'")
        try:
            return import_module(module_name)
        except ModuleNotFoundError:
            logger.trace(f"Module '{module_name}' import failed.")
            if plugin_name != module_name:
                break

            module_name, plugin = module_name.rsplit(".", maxsplit=1)
            logger.trace(f"Consider '{module_name}' as module name and '{plugin}' as plugin name")

    return None


def load_plugins(
    module: ModuleType,
    *,
    plugin_name: str,
) -> List[Type[Plugin]]:
    return []


def create_objects(plugin_classes: List[Type[Plugin]]) -> List[Plugin]:
    return []


class SimplePluginLoader:
    def __call__(self, plugin_name: str) -> List[Plugin]:
        module: Optional[ModuleType] = load_module(plugin_name)
        if not module:
            logger.info(f"Cannot load module by plugin name '{plugin_name}'")
            return []

        plugin_classes: List[Type[Plugin]] = load_plugins(module, plugin_name=plugin_name)

        logger.debug(
            f"Plugins loaded by plugin name '{plugin_name}': {[p.__name__ for p in plugin_classes]}"
        )

        plugin_objects: List[Plugin] = create_objects(plugin_classes)

        return plugin_objects

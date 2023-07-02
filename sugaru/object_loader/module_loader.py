from importlib import import_module
from types import ModuleType
from typing import Optional

from ..logging import logger


def load_module(plugin_name: str) -> Optional[ModuleType]:
    module_name: str = plugin_name
    while True:
        logger.trace(f"Try to import module by name '{module_name}'")
        try:
            return import_module(module_name)
        except ModuleNotFoundError as exc:
            logger.trace(f"Module '{module_name}' import failed ({exc}).")
            if plugin_name != module_name or "." not in module_name:
                break

            module_name, plugin = module_name.rsplit(".", maxsplit=1)
            logger.trace(f"Consider '{module_name}' as module name and '{plugin}' as plugin name")

    return None

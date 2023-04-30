from importlib import import_module
from inspect import Signature, getmembers, isclass, isfunction, signature
from types import ModuleType
from typing import Any, Dict, List, Optional, Type

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


def load_objects(
    module: ModuleType,
    *,
    plugin_name: str,
) -> List[Type[Plugin]]:
    if module.__name__ == plugin_name:
        logger.trace(f"Loading all module '{plugin_name}' objects")
        return [
            v for _, v in getmembers(module, predicate=lambda obj: isclass(obj) or isfunction(obj))
        ]
    else:
        module_name, plugin_name = plugin_name.rsplit(".", maxsplit=1)
        logger.trace(f"Loading single object '{plugin_name}' in module '{module_name}'")
        try:
            return [getattr(module, plugin_name)]
        except AttributeError:
            logger.warning(f"No object called '{plugin_name}' found in module {module.__name__}")
            return []


def check_plugins_signatures(object_classes: List[Type[Plugin]]) -> List[Type[Plugin]]:
    standard: Signature = signature(Plugin.__call__)
    standard_params: Dict[str, Any] = {
        p.name: p.annotation
        for p in standard.parameters.values()
        if p.name not in ("self", "kwargs")
    }
    plugin_classes: List[Type[Plugin]] = []
    for obj in object_classes:
        sign: Signature
        if isclass(obj) and hasattr(obj, "__call__"):
            logger.trace(f"Plugin '{obj.__name__}' is a class and callable")
            sign = signature(obj.__call__)
        elif isfunction(obj):
            logger.trace(f"Plugin '{obj.__name__}' is a function")
            sign = signature(obj)
        else:
            logger.trace(
                f"Plugin '{obj.__name__}' is neither class with __call__ nor function. skip"
            )
            continue

        obj_params: Dict[str, Any] = {
            p.name: p.annotation
            for p in standard.parameters.values()
            if p.name not in ("self", "kwargs")
        }

        if obj_params != standard_params or sign.return_annotation != standard.return_annotation:
            logger.warning(
                f"Plugin '{obj.__name__}' has bad signature. Please, check class 'Plugin' signature."
            )
            continue

        plugin_classes.append(obj)

    return plugin_classes


def create_objects(plugin_classes: List[Type[Plugin]]) -> List[Plugin]:
    return []


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

        plugin_objects: List[Plugin] = create_objects(plugin_classes)

        def plug_name(obj):
            return obj.__name__ if isfunction(obj) else type(obj).__name__

        logger.debug(
            f"Plugin '{plugin_name}' objects after plugin class instantiating: {[plug_name(p) for p in plugin_objects]}"
        )

        return plugin_objects

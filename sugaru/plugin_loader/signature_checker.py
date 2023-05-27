import builtins
from inspect import Signature, isclass, isfunction, signature
from typing import Any, Dict, List, Type

from ..interfaces import Plugin
from ..logging import logger


def check_plugins_signatures(object_classes: List[Type[Plugin]]) -> List[Type[Plugin]]:
    standard: Signature = signature(Plugin.__call__)
    standard_params: Dict[str, Any] = {
        p.name: p.annotation
        for p in standard.parameters.values()
        if p.name not in ("self", "kwargs")
    }
    plugin_classes: List[Type[Plugin]] = []
    builtin_types: List[str] = dir(builtins)
    for obj in object_classes:
        if obj.__name__ in builtin_types:
            continue

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
            for p in sign.parameters.values()
            if p.name not in ("self", "kwargs")
        }

        if obj_params != standard_params or sign.return_annotation != standard.return_annotation:
            logger.warning(
                f"Plugin '{obj.__name__}' has bad signature. Please, check class 'Plugin' signature."
            )
            continue

        plugin_classes.append(obj)

    return plugin_classes

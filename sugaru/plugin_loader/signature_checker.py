from inspect import Signature, signature
from typing import List, Type

from ..interfaces import Plugin
from ..utils import check_callable_signature


def check_plugins_signatures(
    object_classes: List[Type[Plugin]],
    type_check: bool = True,
) -> List[Type[Plugin]]:
    standard: Signature = signature(Plugin.__call__)
    {
        p.name: p.annotation
        for p in standard.parameters.values()
        if p.name not in ("self", "kwargs")
    }
    plugin_classes: List[Type[Plugin]] = []
    for obj in object_classes:
        if check_callable_signature(obj, Plugin, type_check=type_check):
            plugin_classes.append(obj)

    return plugin_classes

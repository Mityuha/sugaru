from inspect import isclass, isfunction
from typing import Optional, Type

from ..interfaces import Plugin


def create_object(plugin_class: Type[Plugin]) -> Optional[Plugin]:
    if isclass(plugin_class):
        try:
            return plugin_class()
        except TypeError:
            return None

    elif isfunction(plugin_class):
        return plugin_class

    return None

from inspect import isclass, isfunction
from typing import Callable, Optional, Type, TypeVar


T = TypeVar("T")


def create_object(plugin_class: Type[T]) -> Optional[Callable]:
    if isclass(plugin_class):
        try:
            return plugin_class()
        except TypeError:
            return None

    elif isfunction(plugin_class):
        return plugin_class

    return None

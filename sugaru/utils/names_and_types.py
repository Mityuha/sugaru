import builtins
import typing
from types import FunctionType
from typing import Any, Set, Type, Union

import typing_extensions


__all__ = ["BUILTIN_TYPES", "callable_name", "is_builtin"]

BUILTIN_TYPES: Set[str] = set(dir(builtins) + dir(typing) + dir(typing_extensions))


def is_builtin(_type: Union[Type, FunctionType]) -> bool:
    return _type.__name__ in BUILTIN_TYPES


def callable_name(obj: Any) -> str:
    if hasattr(obj, "__name__"):
        return obj.__name__

    return type(obj).__name__

import builtins
from types import FunctionType
from typing import Any, List, Type, Union


BUILTIN_TYPES: List[str] = dir(builtins)


def is_builtin(_type: Union[Type, FunctionType]) -> bool:
    return _type.__name__ in BUILTIN_TYPES


def callable_name(obj: Any) -> str:
    if hasattr(obj, "__name__"):
        return obj.__name__

    return type(obj).__name__

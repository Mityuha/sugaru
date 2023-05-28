import builtins
from types import FunctionType
from typing import List, Type


BUILTIN_TYPES: List[str] = dir(builtins)


def is_builtin(_type: Type | FunctionType) -> bool:
    return _type.__name__ in BUILTIN_TYPES

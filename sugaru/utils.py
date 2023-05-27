import builtins
from inspect import Signature, isclass, isfunction, signature
from types import FunctionType
from typing import Any, Dict, List, Type

from .logging import logger


__all__ = ["check_callable_signature", "is_builtin"]


BUILTIN_TYPES: List[str] = dir(builtins)


def is_builtin(_type: Type | FunctionType) -> bool:
    return _type.__name__ in BUILTIN_TYPES


def check_callable_signature(
    obj: Type[Any],
    class_: Type[Any],
    *,
    type_check: bool = False,
) -> bool:
    standard: Signature = signature(class_.__call__)

    standard_params: Dict[str, Any] = {
        p.name: p.annotation
        for p in standard.parameters.values()
        if p.name not in ("self", "args", "kwargs")
    }

    if is_builtin(obj):
        return False

    sign: Signature

    if isclass(obj) and hasattr(obj, "__call__"):
        logger.trace(f"Object '{obj.__name__}' is a class and callable")
        sign = signature(obj.__call__)
    elif isfunction(obj):
        logger.trace(f"Object '{obj.__name__}' is a function")
        sign = signature(obj)
    else:
        logger.trace(f"Object '{obj.__name__}' is neither class with __call__ nor function. skip")
        return False

    obj_params: Dict[str, Any] = {
        p.name: p.annotation for p in sign.parameters.values() if p.name not in ("self", "kwargs")
    }

    if obj_params.keys() != standard_params.keys():
        logger.info(f"Object '{object.__name__}' has got bad param names")
        return False

    if type_check:
        logger.warning(
            "'type_check' option is not implemented yet"
            "The thing is consider 'dict' and 'typing.Dict' types as the same types"
        )

    return True

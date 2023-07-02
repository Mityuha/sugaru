from inspect import Signature, isclass, isfunction, signature
from types import FunctionType
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from ..interfaces import Plugin
from ..logging import logger
from ..utils import callable_name
from .names_and_types import is_builtin


__all__ = [
    "callable_params",
    "callable_signature",
    "check_callable_signature",
    "signature_params",
    "signature_type_check",
]


def callable_signature(obj: Union[Type[Any], FunctionType]) -> Optional[Signature]:
    sign: Optional[Signature] = None

    if isclass(obj) and hasattr(obj, "__call__"):
        logger.trace(f"Object '{callable_name(obj)}' is a class and callable")
        sign = signature(obj.__call__)
    elif isfunction(obj):
        logger.trace(f"Object '{callable_name(obj)}' is a function")
        sign = signature(obj)
    else:
        logger.trace(
            f"Object '{callable_name(obj)}' is neither class with __call__ nor function. skip"
        )

    return sign


def signature_params(
    sign: Signature,
    *,
    ignore_names: Tuple = ("self", "args", "kwargs"),
) -> Dict[str, Any]:
    return {p.name: p.annotation for p in sign.parameters.values() if p.name not in ignore_names}


def callable_params(obj: Callable) -> Dict[str, Any]:
    sign: Optional[Signature]
    if isfunction(obj):
        sign = callable_signature(obj)
    else:
        sign = callable_signature(type(obj))

    if not sign:
        raise ValueError(f"Object '{callable_name(obj)}' is not callable")

    return signature_params(sign)


def signature_type_check(*, check: Signature, origin: Signature) -> bool:
    logger.info("'type_check' option is not implemented yet")
    return True


def check_callable_signature(
    obj: Type[Any],
    class_: Type[Any],
    *,
    type_check: bool = False,
) -> bool:
    obj_sign: Optional[Signature] = callable_signature(obj)
    if is_builtin(obj) or not obj_sign:
        return False

    cls_sign: Signature = signature(class_.__call__)

    obj_params: Dict[str, Any] = signature_params(obj_sign)
    cls_params: Dict[str, Any] = signature_params(cls_sign)

    if class_ is not Plugin:
        if obj_params.keys() != cls_params.keys():
            logger.trace(f"Object '{callable_name(obj)}' has got bad param names")
            return False
    else:
        if not set(obj_params.keys()).intersection(set(cls_params.keys())):
            logger.trace(
                f"Object '{callable_name(obj)}' is not satisfy any of possible 'Plugin' signatures."
            )
            return False

    if type_check:
        return signature_type_check(check=obj_sign, origin=cls_sign)

    return True

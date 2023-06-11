from inspect import Signature, isclass, isfunction, signature
from typing import Any, Dict, Optional, Tuple, Type

from ..interfaces import Plugin
from ..logging import logger
from ..utils import callable_name
from .names_and_types import is_builtin


def callable_signature(obj: Type[Any]) -> Optional[Signature]:
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


def callable_params(
    sign: Signature,
    *,
    ignore_names: Tuple = ("self", "args", "kwargs"),
) -> Dict[str, Any]:
    return {p.name: p.annotation for p in sign.parameters.values() if p.name not in ignore_names}


def callable_type_check(*, obj_sign: Signature, cls_sign: Signature) -> bool:
    logger.info(
        "'type_check' option is not implemented yet"
        "The thing is considering 'dict', 'typing.Dict', 'Mapping' (and so forth) types as the same types"
    )
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

    obj_params: Dict[str, Any] = callable_params(obj_sign)
    cls_params: Dict[str, Any] = callable_params(cls_sign)

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
        return callable_type_check(obj_sign=obj_sign, cls_sign=cls_sign)

    return True

from typing import Callable, List, Type

from ..interfaces import ObjectLoader


__all__ = ["load_object_or_raise_error"]


def load_object_or_raise_error(
    object_loader: ObjectLoader[Callable],
    *,
    obj_name: str,
    class_: Type[Callable],
    type_check: bool,
) -> Callable:
    objects: List[Callable] = object_loader(
        obj_name=obj_name,
        class_=class_,
        type_check=type_check,
    )
    if not objects:
        raise ImportError(f"Cannot load object '{obj_name}' by signature '{class_}'")

    return objects[0]

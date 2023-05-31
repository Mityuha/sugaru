from types import ModuleType
from typing import Callable, Generic, List, Optional, Type, TypeVar

from ..logging import logger
from ..utils import callable_name, check_callable_signature
from .module_loader import load_module
from .object_creator import create_object
from .objects_loader import load_objects


T = TypeVar("T")


class SimpleObjectLoader(Generic[T]):
    def __call__(
        self,
        obj_name: str,
        class_: Type[T],
        *,
        type_check: bool = True,
    ) -> List[Callable]:
        _self: str = f"[{callable_name(class_)} '{obj_name}']"
        module: Optional[ModuleType] = load_module(obj_name)
        if not module:
            logger.info(f"{_self}: Cannot load module by object name '{obj_name}'")
            return []

        any_object_classes: List[Type[T]] = load_objects(module, obj_name=obj_name)

        logger.trace(
            f"{_self}: Objects loaded by object name '{obj_name}': {[obj.__name__ for obj in any_object_classes]}"
        )

        object_classes: List[Type[T]] = [
            obj
            for obj in any_object_classes
            if check_callable_signature(
                obj,
                class_=class_,
                type_check=type_check,
            )
        ]

        logger.trace(
            f"{_self}: classes after signature check: {[p.__name__ for p in object_classes]}"
        )

        objects: List[Callable] = []
        for obj_class in object_classes:
            obj: Optional[Callable] = create_object(obj_class)
            if not obj:
                logger.info(
                    f"{_self}: Object '{callable_name(obj_class)}' can't be created in a simple way. Skip."
                )
                continue
            objects.append(obj)

        logger.trace(
            f"{_self}: objects after classes instantiating: {[callable_name(p) for p in objects]}"
        )

        return objects

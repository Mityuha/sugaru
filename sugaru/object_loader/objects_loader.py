from inspect import getmembers, isclass, isfunction
from types import ModuleType
from typing import List, Type, TypeVar

from ..logging import logger
from ..utils import is_builtin


T = TypeVar("T")


def load_objects(
    module: ModuleType,
    *,
    obj_name: str,
) -> List[Type[T]]:
    if module.__name__ == obj_name:
        logger.trace(f"Loading all module '{obj_name}' objects")
        return [
            v
            for _, v in getmembers(
                module,
                predicate=lambda obj: (isclass(obj) or isfunction(obj)) and not is_builtin(obj),
            )
        ]
    else:
        module_name, obj_name = obj_name.rsplit(".", maxsplit=1)
        logger.trace(f"Loading single object '{obj_name}' in module '{module_name}'")
        try:
            return [getattr(module, obj_name)]
        except AttributeError:
            logger.warning(f"No object called '{obj_name}' found in module {module.__name__}")
            return []

from inspect import getmembers, isclass, isfunction
from types import ModuleType
from typing import List, Type

from ..interfaces import Plugin
from ..logging import logger
from .utils import is_builtin


def load_objects(
    module: ModuleType,
    *,
    plugin_name: str,
) -> List[Type[Plugin]]:
    if module.__name__ == plugin_name:
        logger.trace(f"Loading all module '{plugin_name}' objects")
        return [
            v
            for _, v in getmembers(
                module,
                predicate=lambda obj: (isclass(obj) or isfunction(obj)) and not is_builtin(obj),
            )
        ]
    else:
        module_name, plugin_name = plugin_name.rsplit(".", maxsplit=1)
        logger.trace(f"Loading single object '{plugin_name}' in module '{module_name}'")
        try:
            return [getattr(module, plugin_name)]
        except AttributeError:
            logger.warning(f"No object called '{plugin_name}' found in module {module.__name__}")
            return []

from typing import Dict

from ..interfaces import SugarFileLoader
from ..utils import Final
from .simple_json import loader as simple_json_loader
from .simple_yaml import loader as simple_yaml_loader


loader_by_extension: Final[Dict[str, SugarFileLoader]] = {
    ".yaml": simple_yaml_loader,
    ".yml": simple_yaml_loader,
    ".json": simple_json_loader,
}

import json
from pathlib import Path
from typing import Dict

from ..logging import logger
from ..types import SecName, Section


def loader(path: Path) -> Dict[SecName, Section]:
    with path.open(encoding="utf-8") as load_file:
        return json.load(load_file)

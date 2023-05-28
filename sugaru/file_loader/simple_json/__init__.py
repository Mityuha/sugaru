import json
from pathlib import Path

from ..logging import logger
from ..types import JSON


def loader(path: Path) -> JSON:
    with path.open(encoding="utf-8") as load_file:
        return json.load(load_file)

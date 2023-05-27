import json
import sys
from pathlib import Path

from ..types import SectionMap


def writer(*, path: Path, content: SectionMap) -> None:
    with path.open("w", encoding="utf-8") as json_file:
        json.dump(dict(content), json_file)


def to_stdout(content: SectionMap) -> None:
    json.dump(dict(content), sys.stdout, indent=4)

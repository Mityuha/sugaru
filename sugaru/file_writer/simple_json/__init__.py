import json
import sys
from pathlib import Path

from ..types import JSON


def writer(*, path: Path, content: JSON) -> None:
    with path.open("w", encoding="utf-8") as json_file:
        json.dump(content, json_file)


def to_stdout(content: JSON) -> None:
    json.dump(content, sys.stdout, indent=4)

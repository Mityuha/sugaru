import sys

from ..logging import logger


try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    logger.error("Cannot import module named 'yaml'. Try install 'pyyaml' first and try again")
    raise

from pathlib import Path
from typing import Dict

from ..types import SecName, Section


def writer(*, path: Path, content: Dict[SecName, Section]) -> None:
    with path.open("w", encoding="utf-8") as yaml_file:
        yaml.dump(
            content,
            yaml_file,
            width=1024,
        )


def to_stdout(content: Dict[SecName, Section]) -> None:
    yaml.dump(content, sys.stdout, width=1024)

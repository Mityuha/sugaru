import sys

from ..logging import logger


try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    logger.error("Cannot import module named 'yaml'. Try install 'pyyaml' first and try again")
    raise

from pathlib import Path

from ..types import JSON


def writer(*, path: Path, content: JSON) -> None:
    with path.open("w", encoding="utf-8") as yaml_file:
        yaml.dump(
            content,
            yaml_file,
            width=1024,
        )


def to_stdout(content: JSON) -> None:
    yaml.dump(content, sys.stdout, width=1024)

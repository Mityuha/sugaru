import sys

from ..logging import logger


try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    logger.error("Cannot import module named 'yaml'. Try install 'pyyaml' first and try again")
    raise

from pathlib import Path

from ..types import SectionMap


def writer(*, path: Path, content: SectionMap) -> None:
    with path.open("w", encoding="utf-8") as yaml_file:
        yaml.dump(
            dict(content),
            yaml_file,
            width=1024,
        )


def to_stdout(content: SectionMap) -> None:
    yaml.dump(dict(content), sys.stdout, width=1024)

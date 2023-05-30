from ..logging import logger


try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    logger.error("Cannot import module named 'yaml'. Try install 'pyyaml' first and try again")
    raise
from pathlib import Path

from sugaru.utils import Final
from ..types import JSON


class Ref(yaml.YAMLObject):
    yaml_tag = "!reference"
    yaml_loader = yaml.SafeLoader

    def __init__(self, values: yaml.nodes.CollectionNode) -> None:
        self._values: Final[yaml.nodes.CollectionNode] = values

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(loader.construct_sequence(node))

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_sequence(
            cls.yaml_tag,
            data._values,
        )


def loader(path: Path) -> JSON:
    with path.open(encoding="utf-8") as load_file:
        return yaml.safe_load(load_file)

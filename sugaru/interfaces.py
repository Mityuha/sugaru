from pathlib import Path
from typing import Any, Dict, List, Protocol, runtime_checkable

from .types import JSON, SecName, Section


__all__ = [
    "FinalFileWriter",
    "Plugin",
    "PluginLoader",
    "SugarFileLoader",
]


@runtime_checkable
class Plugin(Protocol):
    def __call__(
        self,
        *,
        section: Section,
        section_name: str,
        sections: Dict[SecName, Section],
        **kwargs: Any,
    ) -> Section:
        ...


class SugarFileLoader(Protocol):
    def __call__(self, path: Path) -> JSON:
        ...


class FinalFileWriter(Protocol):
    def __call__(self, *, path: Path, content: JSON) -> None:
        ...


class PluginLoader(Protocol):
    def __call__(
        self,
        plugin_name: str,
    ) -> List[Plugin]:
        ...


class SectionEncoder(Protocol):
    def __call__(self, content: JSON) -> Dict[SecName, Section]:
        ...


class SectionDecoder(Protocol):
    def __call__(self, section_map: Dict[SecName, Section], *, origin: JSON) -> JSON:
        ...

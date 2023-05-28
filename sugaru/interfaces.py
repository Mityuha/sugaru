from pathlib import Path
from typing import Any, List, Protocol, runtime_checkable

from .types import JSON, Section, SectionMap


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
        sections: SectionMap,
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

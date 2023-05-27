from pathlib import Path
from typing import Any, Dict, Optional, Protocol, runtime_checkable

from .types import SecName, Section, SectionMap


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
    def __call__(self, path: Path) -> Dict[SecName, Section]:
        ...


class FinalFileWriter(Protocol):
    def __call__(self, *, path: Path, content: Dict[SecName, Section]) -> None:
        ...


class PluginLoader(Protocol):
    def __call__(
        self,
        plugin_name: str,
    ) -> Optional[Plugin]:
        ...

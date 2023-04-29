from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from .types import SecName, Section


__all__ = [
    "FinalFileWriter",
    "Plugin",
    "PluginLoader",
    "PluginNamesFetcher",
    "SugarFileLoader",
]


@runtime_checkable
class Plugin(Protocol):
    def __call__(
        self,
        *,
        section_body: Dict[str, Section],
        section_name: SecName = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
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
        *,
        path_candidates: List[Path],
    ) -> Optional[Plugin]:
        ...


class PluginNamesFetcher(Protocol):
    def __call__(self) -> List[str]:
        ...

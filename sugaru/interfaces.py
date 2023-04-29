from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


__all__ = [
    "Plugin",
    "SugarFileLoader",
    "FinalFileWriter",
    "PluginLoader",
    "PluginNamesFetcher",
]


@runtime_checkable
class Plugin(Protocol):
    def __call__(
        self,
        *,
        section_body: Dict[str, Any],
        section_name: str = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        ...


class SugarFileLoader(Protocol):
    def __call__(self, path: Path) -> Dict[str, Any]:
        ...


class FinalFileWriter(Protocol):
    def __call__(self, *, path: Path, content: Dict[str, Any]) -> None:
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

from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class Plugin(Protocol):
    def parse(
        self,
        *,
        section_body: Dict[str, Any],
        section_name: str = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        ...


class SugarFileLoader(Protocol):
    def load(self, path: Path) -> Dict[str, Any]:
        ...


class FinalFileWriter(Protocol):
    def write(self, *, path: Path, content: Dict[str, Any]) -> None:
        ...


class PluginLoader(Protocol):
    def load(
        self,
        plugin_name: str,
        *,
        path_candidates: List[Path],
    ) -> Optional[Plugin]:
        ...


class PluginNamesFetcher(Protocol):
    def plugin_name_list(self) -> List[str]:
        ...

import sys
from pathlib import Path
from typing import Dict, List, Mapping, Type, TypeVar


if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from .types import JSON, SecName, Section


T = TypeVar("T")

__all__ = [
    "FinalFileWriter",
    "ObjectLoader",
    "Plugin",
    "PluginExecutor",
    "SectionDecoder",
    "SectionEncoder",
    "SugarFileLoader",
]


class Plugin(Protocol):
    def __call__(
        self,
        *,
        section: Section,
        section_name: str,
        sections: Mapping[SecName, Section],
    ) -> Section:
        ...


class SugarFileLoader(Protocol):
    def __call__(self, path: Path) -> JSON:
        ...


class FinalFileWriter(Protocol):
    def __call__(self, *, path: Path, content: JSON) -> None:
        ...


class ObjectLoader(Protocol[T]):
    def __call__(
        self,
        obj_name: str,
        class_: Type[T],
        *,
        type_check: bool = True,
    ) -> List[T]:
        ...


class SectionEncoder(Protocol):
    def __call__(self, content: JSON) -> Dict[SecName, Section]:
        ...


class SectionDecoder(Protocol):
    def __call__(self, sections: Dict[SecName, Section], *, origin: JSON) -> JSON:
        ...


class PluginExecutor(Protocol):
    def __call__(
        self,
        *,
        sections: Mapping[str, Section],
        plugins: Mapping[str, Plugin],
    ) -> Dict[str, Section]:
        ...

from pathlib import Path
from typing import Any, Dict, List, Protocol, Type, TypeVar

from .types import JSON, SecName, Section


T = TypeVar("T")

__all__ = [
    "FinalFileWriter",
    "ObjectLoader",
    "Plugin",
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
    def __call__(self, section_map: Dict[SecName, Section], *, origin: JSON) -> JSON:
        ...

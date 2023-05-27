from types import MappingProxyType
from typing import Dict, List


__all__ = ["JSON", "SecName", "Section", "SectionMap"]

JSON = Dict[str, "JSON"] | List["JSON"] | str | int | float | bool | None
Section = JSON
SecName = str
SectionMap = MappingProxyType[SecName, Section]

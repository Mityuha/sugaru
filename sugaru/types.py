from typing import Dict, List


__all__ = ["JSON", "SecName", "Section"]

JSON = Dict[str, "JSON"] | List["JSON"] | str | int | float | bool | None
Section = JSON
SecName = str

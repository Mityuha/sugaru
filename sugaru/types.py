from typing import Dict, List, Union


__all__ = ["JSON", "SecName", "Section"]

JSON = Union[
    Dict[str, "JSON"],
    List["JSON"],
    str,
    int,
    float,
    bool,
    None,
]
Section = JSON
SecName = str

from typing import Any, Dict, List, Union


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

# Section = Union[JSON, BaseTypedDict, Mapping[str, Any], Dict[str, Any]]
Section = Any  # In fact, section is anything at all
SecName = str

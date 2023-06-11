from typing import Any, Dict, List, TypedDict, Union


__all__ = ["JSON", "SecName", "Section"]


class BaseTypedDict(TypedDict):
    ...


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

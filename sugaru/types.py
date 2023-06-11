from typing import Dict, List, TypedDict, Union


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
    BaseTypedDict,
]
Section = JSON
SecName = str

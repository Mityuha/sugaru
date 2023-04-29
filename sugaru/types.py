from typing import Dict, List


JSON = Dict[str, "JSON"] | List["JSON"] | str | int | float | bool | None
Section = JSON
SecName = str

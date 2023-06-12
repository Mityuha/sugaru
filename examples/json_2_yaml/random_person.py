from random import choice
from typing import Dict, Final, List, Union


VALUES: Final[Dict[str, List[Union[str, int]]]] = {
    "{first_name}": ["John", "James", "Rob"],
    "{second_name}": ["Celvin", "Bond", "Williams"],
    "{age}": [i for i in range(20, 43)],
    "{job_title}": ["Manager", "CIO", "Engineer"],
}


def random_person(section: str) -> Union[str, int]:
    if section not in VALUES:
        raise ValueError(f"Bad value '{section}'." "Available values: {list(VALUES.keys())}")

    return choice(VALUES[section])

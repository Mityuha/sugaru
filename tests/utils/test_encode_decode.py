from typing import Dict

import pytest
from faker import Faker

from sugaru import JSON, Section
from sugaru.utils import decode_section, encode_section


faker = Faker()


@pytest.mark.parametrize(
    "content",
    [
        faker.pydict(value_types=[int, str]),
        faker.pylist(value_types=[int, str]),
        faker.pystr(),
        faker.pyint(),
        faker.pyfloat(),
        faker.pybool(),
        None,
    ],
)
def test_encode_decode(content: JSON) -> None:
    section_map: Dict[str, Section] = encode_section(content)
    content_got: JSON = decode_section(section_map, origin=content)

    assert content == content_got

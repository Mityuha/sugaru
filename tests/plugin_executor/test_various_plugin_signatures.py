from typing import Callable, Dict

import pytest

from sugaru import Section, simple_plugin_executor


@pytest.mark.parametrize(
    "plugin",
    [
        lambda section_name, section, sections: section,
        lambda section: section,
        lambda section_name: {},
        lambda sections: {},
        lambda section_name, section: section,
        lambda section_name, sections: {},
        lambda section, sections: {},
    ],
)
def test_full_plugin_signature(plugin: Callable) -> None:
    sections: Dict[str, Section] = {"": {}}

    sugar_sections = simple_plugin_executor(sections=sections, plugins={"test_plugin": plugin})

    assert sugar_sections == sections

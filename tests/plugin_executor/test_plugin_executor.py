from typing import Dict, Mapping

import pytest

from sugaru import Section, simple_plugin_executor


def test_plugin_executor_merge() -> None:
    def append_1_plugin(
        section_name: str, section: Section, sections: Mapping[str, Section]
    ) -> Section:
        section["key"].append(1)  # type: ignore
        return section

    def append_2_plugin(
        section_name: str, section: Section, sections: Mapping[str, Section]
    ) -> Section:
        section["key"].append(2)  # type: ignore
        return section

    sections: Dict[str, Section] = {"": {"key": []}}
    sugar_sections: Dict[str, Section] = simple_plugin_executor(
        sections=sections,
        plugins={"1": append_1_plugin, "2": append_2_plugin},
    )

    assert sections == {"": {"key": []}}
    assert sugar_sections[""]["key"] == [1, 2]  # type: ignore

    sugar_sections = simple_plugin_executor(
        sections=sections,
        plugins={"2": append_2_plugin, "1": append_1_plugin},
    )

    assert sugar_sections[""]["key"] == [2, 1]  # type: ignore


def test_section_update_is_forbidden() -> None:
    def modify_sections_plugin(
        section_name: str, section: Section, sections: Mapping[str, Section]
    ) -> Section:
        assert section == "section"
        sections.update({"update": "forbidden"})  # type: ignore
        return section

    with pytest.raises(RuntimeError):
        simple_plugin_executor(
            sections={"some": "section"},
            plugins={"bad": modify_sections_plugin},
        )

from copy import deepcopy
from typing import Dict, Mapping, cast

from ..interfaces import Plugin
from ..logging import logger
from ..types import SecName, Section


def simple_plugin_executor(
    *,
    sections: Mapping[str, Section],
    plugins: Mapping[str, Plugin],
) -> Dict[str, Section]:
    sugar_sections: Dict[SecName, Section] = {}

    section: Section
    section_name: str
    plugin_name: str
    plugin: Plugin

    sections_template: Mapping[str, Section] = deepcopy(sections)

    for section_name, section in sections.items():
        for plugin_name, plugin in plugins.items():
            section_to_pass: Section = cast(
                Section,
                deepcopy(
                    sugar_sections.get(section_name, section),
                ),
            )

            new_section: Section = plugin(
                section_name=section_name,
                section=section_to_pass,
                sections=sections,
            )

            if new_section != section_to_pass:
                logger.trace(f"Section '{section_name}' was modified by plugin '{plugin_name}'")

            sugar_sections[section_name] = new_section

            if sections != sections_template:
                raise RuntimeError(
                    f"Plugin '{plugin_name}' modified sections, but it's forbidden."
                )

    _ = [
        sugar_sections.setdefault(section_name, section)
        for section_name, section in sections.items()
    ]

    return sugar_sections

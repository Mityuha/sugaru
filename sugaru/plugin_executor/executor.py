from copy import deepcopy
from typing import Any, Dict, Mapping

from ..interfaces import Plugin
from ..logging import logger
from ..types import SecName, Section
from ..utils import callable_params


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
            plugin_params: Dict[str, Any] = callable_params(plugin)

            values: Dict[str, Any] = {
                "section_name": section_name,
                "sections": sections,
            }
            if "section" in plugin_params:
                values["section"] = deepcopy(sugar_sections.get(section_name, section))

            kwargs: Dict[str, Any] = {
                param_name: values[param_name] for param_name in plugin_params
            }

            new_section: Section = plugin(**kwargs)

            if kwargs.get("section") and new_section != kwargs["section"]:
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

from pathlib import Path
from types import MappingProxyType
from typing import Any, Dict, List

from .interfaces import FinalFileWriter, Plugin, PluginLoader, SugarFileLoader
from .logging import logger
from .types import SecName, Section, SectionMap


__all__ = ["sugarate"]


def immutable_section_map(mutable_sections: Dict[SecName, Section]) -> SectionMap:
    sections: Any = {}
    for name, section in mutable_sections.items():
        new_section: Any = section
        if isinstance(section, dict):
            new_section = MappingProxyType(section)
        elif isinstance(section, list):
            new_section = tuple(section)

        sections[name] = new_section

    return sections


def section_to_mutable_section(section: Any) -> Section:
    if isinstance(section, MappingProxyType):
        return dict(section)

    return section


def sugarate(
    *,
    plugin_name_list: List[str],
    plugin_loader: PluginLoader,
    sugar_file_path: Path,
    sugar_file_loader: SugarFileLoader,
    final_file_path: Path,
    final_file_writer: FinalFileWriter,
) -> None:
    logger.debug(f"Plugin list: {plugin_name_list}")

    plugin_name: str
    plugins: Dict[str, Plugin] = {}
    for plugin_name in plugin_name_list:
        plugin_list: List[Plugin] = plugin_loader(plugin_name)
        print(">>>", plugin_list)
        if not plugin_list:
            logger.warning(f"Unable to load plugin '{plugin_name}', skip")
            continue

        for plugin in plugin_list:
            plugins[f"{plugin_name}{str(plugin)}"] = plugin  # TODO

    if not plugins:
        logger.warning("No one plugin was loaded, returning...")
        return

    logger.debug(f"Plugins loaded: {list(plugins.keys())}")

    logger.trace(f"Loading file '{sugar_file_path.name}'")
    mutable_sections: Dict[SecName, Section] = sugar_file_loader(sugar_file_path)  # type: ignore # TODO
    immutable_sections: SectionMap = immutable_section_map(mutable_sections)
    sugar_sections: Dict[SecName, Section] = {}

    logger.trace(f"File '{sugar_file_path.name}' successfully loaded")

    section: Section
    section_name: str
    for section_name, section in immutable_sections.items():
        for plugin_name, plugin in plugins.items():
            new_section: Section = plugin(
                section_name=section_name,
                section=section,
                sections=immutable_sections,
            )

            sugar_sections[section_name] = section_to_mutable_section(new_section)

            if (new_section != section) and (section_name in sugar_sections):
                logger.warning(
                    f"Section '{section_name}' was previously modified "
                    f"and now that modified version is overwritten by plugin '{plugin_name}'."
                )

    _ = [
        sugar_sections.setdefault(section_name, section)
        for section_name, section in mutable_sections.items()
    ]

    final_file_writer(path=final_file_path, content=sugar_sections)

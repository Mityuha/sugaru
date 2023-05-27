from pathlib import Path
from types import MappingProxyType
from typing import Any, Dict, List, Optional

from .interfaces import FinalFileWriter, Plugin, PluginLoader, PluginNamesFetcher, SugarFileLoader
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


def sugarate(
    *,
    plugin_name_list: List[str],
    plugin_names_fetcher: PluginNamesFetcher,
    plugin_loader: PluginLoader,
    sugar_file_path: Path,
    sugar_file_loader: SugarFileLoader,
    final_file_path: Path,
    final_file_writer: FinalFileWriter,
) -> None:
    if not plugin_name_list:
        plugin_name_list = plugin_names_fetcher()

    if not plugin_name_list:
        logger.info("No plugins were specified or fetched, returning...")
        return

    logger.debug(f"Plugin list specified or fetched: {plugin_name_list}")

    plugin_name: str
    plugins: Dict[str, Plugin] = {}
    for plugin_name in plugin_name_list:
        plugin: Optional[Plugin] = plugin_loader(plugin_name)
        if not plugin:
            logger.warning(f"Unable to load plugin '{plugin_name}', skip")
            continue

        plugins[plugin_name] = plugin

    if not plugins:
        logger.warning("No one plugin was loaded, returning...")
        return

    logger.debug(f"Plugins loaded: {list(plugins.keys())}")

    sections: SectionMap = immutable_section_map(sugar_file_loader(sugar_file_path))
    sugar_sections: Dict[SecName, Section] = {}

    section: Section
    section_name: str
    for section_name, section in sections.items():
        for plugin_name, plugin in plugins.items():
            plugin(
                section_name=section_name,
                section=section,
                sections=sections,
            )
            sugar_sections[section_name] = sugar_sections

    final_file_writer(path=final_file_path, content=sugar_sections)

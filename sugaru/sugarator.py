from pathlib import Path
from typing import Dict, List, Optional

from .interfaces import FinalFileWriter, Plugin, PluginLoader, PluginNamesFetcher, SugarFileLoader
from .logging import logger
from .types import SecName, Section


__all__ = ["sugarate"]


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
        plugin: Optional[Plugin] = plugin_loader(
            plugin_name,
            path_candidates=[],
        )
        if not plugin:
            logger.warning(f"Unable to load plugin '{plugin_name}', skip")
            continue

        plugins[plugin_name] = plugin

    if not plugins:
        logger.warning("No one plugin was loaded, returning...")
        return

    logger.debug(f"Plugins loaded: {list(plugins.keys())}")

    sections: Dict[SecName, Section] = sugar_file_loader(sugar_file_path)
    sugar_sections: Dict[SecName, Section] = dict(sections)  # deep copy should be here

    section: Section
    section_name: str
    for section_name, section in sections.items():
        for plugin_name, plugin in plugins.items():
            plugin(
                section_name=section_name,
                section=section,
            )
            sugar_sections[section_name] = sugar_sections

    final_file_writer(path=final_file_path, content=sugar_sections)

from pathlib import Path
from typing import List

from .interfaces import FinalFileWriter, PluginLoader, PluginNamesFetcher, SugarFileLoader
from .logging import logger


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
        logger.info("No plugins were specified or loaded, returning...")
        return

    logger.debug(f"Plugin list specified/loaded: {plugin_name_list}")

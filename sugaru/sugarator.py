from pathlib import Path
from typing import Dict, List

from .interfaces import (
    FinalFileWriter,
    ObjectLoader,
    Plugin,
    PluginExecutor,
    SectionDecoder,
    SectionEncoder,
    SugarFileLoader,
)
from .logging import logger
from .types import JSON, SecName, Section
from .utils import callable_name


__all__ = ["sugarate"]


def sugarate(
    *,
    plugin_name_list: List[str],
    object_loader: ObjectLoader,
    sugar_file_path: Path,
    sugar_file_loader: SugarFileLoader,
    final_file_path: Path,
    final_file_writer: FinalFileWriter,
    section_encoder: SectionEncoder,
    section_decoder: SectionDecoder,
    plugin_executor: PluginExecutor,
    type_check: bool = True,
) -> None:
    logger.trace(f"Plugin list: {plugin_name_list}")

    plugin_name: str
    plugins: Dict[str, Plugin] = {}
    for plugin_name in plugin_name_list:
        plugin_list: List[Plugin] = object_loader(
            plugin_name,
            class_=Plugin,
            type_check=type_check,
        )
        if not plugin_list:
            logger.warning(f"Unable to load plugin '{plugin_name}', skip")
            continue

        for plugin in plugin_list:
            plugins[f"{plugin_name}.{callable_name(plugin)}"] = plugin

    if not plugins:
        logger.warning("No one plugin was loaded, returning...")
        return

    logger.trace(f"Plugins loaded: {list(plugins.keys())}")

    logger.trace(f"Loading file '{sugar_file_path.name}'")
    content: JSON = sugar_file_loader(sugar_file_path)
    sections: Dict[SecName, Section] = section_encoder(content)

    logger.trace(f"File '{sugar_file_path.name}' successfully loaded")

    sugar_sections: Dict[str, Section] = plugin_executor(
        sections=sections,
        plugins=plugins,
    )

    logger.trace("All plugins were successfully applied. Decoding sections...")

    output_content: JSON = section_decoder(sugar_sections, origin=content)

    logger.trace("Sections were successfully decoded. Writing content to file...")
    final_file_writer(path=final_file_path, content=output_content)

from pathlib import Path
from typing import Dict, List

from .interfaces import (
    FinalFileWriter,
    ObjectLoader,
    Plugin,
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
    type_check: bool = True,
) -> None:
    logger.debug(f"Plugin list: {plugin_name_list}")

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

    logger.debug(f"Plugins loaded: {list(plugins.keys())}")

    logger.trace(f"Loading file '{sugar_file_path.name}'")
    content: JSON = sugar_file_loader(sugar_file_path)
    sections: Dict[SecName, Section] = section_encoder(content)

    sugar_sections: Dict[SecName, Section] = {}

    logger.trace(f"File '{sugar_file_path.name}' successfully loaded")

    section: Section
    section_name: str

    for section_name, section in sections.items():
        for plugin_name, plugin in plugins.items():
            # TODO:
            # 1. deepcopy(section)
            # 2. check that sections are not changed
            # 3. Merge section content
            # 4. Optional: link section changes to plugin names
            # (simple debugging)

            new_section: Section = plugin(
                section_name=section_name,
                section=section,
                sections=sections,
            )

            if (new_section != section) and (section_name in sugar_sections):
                logger.warning(
                    f"Section '{section_name}' was previously modified "
                    f"and now that modified version is overwritten by plugin '{plugin_name}' [TODO merge]."
                )
            sugar_sections[section_name] = new_section

    _ = [
        sugar_sections.setdefault(section_name, section)
        for section_name, section in sections.items()
    ]

    output_content: JSON = section_decoder(sugar_sections, origin=content)

    final_file_writer(path=final_file_path, content=output_content)

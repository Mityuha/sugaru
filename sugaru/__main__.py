from enum import Enum
from pathlib import Path
from typing import List

import typer

from .file_loader import loader_by_extension
from .file_writer import stdout_writer_by_extension, writer_by_extension
from .interfaces import (
    FinalFileWriter,
    ObjectLoader,
    PluginExecutor,
    SectionDecoder,
    SectionEncoder,
    SugarFileLoader,
)
from .logging import LogLevel, logger, set_log_level
from .object_loader import SimpleObjectLoader
from .plugin_executor import simple_plugin_executor
from .sugarator import sugarate
from .utils import Final, decode_section, encode_section, load_object_or_raise_error


STDOUT: Final[str] = "stdout"
AUTO: Final[str] = "auto"

app = typer.Typer()


@app.command()
def main(
    file: str,
    plugin: List[str] = typer.Option(...),
    *,
    output: str = STDOUT,
    obj_loader: str = AUTO,
    file_loader: str = AUTO,
    file_writer: str = AUTO,
    sec_encoder: str = AUTO,
    sec_decoder: str = AUTO,
    plug_executor: str = AUTO,
    log_level: Enum("", {level.name: level.name for level in LogLevel}) = LogLevel.INFO.name,  # type: ignore
) -> None:
    set_log_level(LogLevel[log_level.value])
    file_path: Path = Path(file)
    if not file_path.is_file():
        logger.warning(f"File '{file}' does not exist or is not a file")
        return

    object_loader: ObjectLoader = SimpleObjectLoader()
    if obj_loader != AUTO:
        object_loader = load_object_or_raise_error(
            object_loader,
            obj_name=obj_loader,
            class_=ObjectLoader,
            type_check=False,
        )

    sugar_file_loader: SugarFileLoader
    if file_loader != AUTO:
        sugar_file_loader = load_object_or_raise_error(
            object_loader,
            obj_name=file_loader,
            class_=SugarFileLoader,
            type_check=False,
        )
    else:
        ext: str = file_path.suffix
        if ext not in loader_by_extension:
            logger.warning(f"Cannot find plugin loader by extension '{ext}'")
            return

        sugar_file_loader = loader_by_extension[ext]

    sugar_file_writer: FinalFileWriter

    output_path: Path = file_path
    if file_writer != AUTO:
        sugar_file_writer = load_object_or_raise_error(
            object_loader,
            obj_name=file_writer,
            class_=FinalFileWriter,
            type_check=False,
        )
    else:
        write_obj_by_ext = stdout_writer_by_extension
        out_ext: str = file_path.suffix

        if output != STDOUT:
            output_path = Path(output)
            out_ext = output_path.suffix
            write_obj_by_ext = writer_by_extension

        if out_ext not in write_obj_by_ext:
            logger.warning(f"cannot find plugin writer by extension '{out_ext}'")
            return

        sugar_file_writer = write_obj_by_ext[out_ext]

    section_encoder: SectionEncoder = encode_section
    section_decoder: SectionDecoder = decode_section

    if sec_encoder != AUTO:
        section_encoder = load_object_or_raise_error(
            object_loader,
            obj_name=sec_encoder,
            class_=SectionEncoder,
            type_check=False,
        )

    if sec_decoder != AUTO:
        section_decoder = load_object_or_raise_error(
            object_loader,
            obj_name=sec_decoder,
            class_=SectionDecoder,
            type_check=False,
        )

    plugin_executor: PluginExecutor = simple_plugin_executor
    if plug_executor != AUTO:
        plugin_executor = load_object_or_raise_error(
            object_loader,
            obj_name=plug_executor,
            class_=PluginExecutor,
            type_check=False,
        )

    sugarate(
        plugin_name_list=plugin,
        object_loader=object_loader,
        sugar_file_path=file_path,
        sugar_file_loader=sugar_file_loader,
        final_file_path=output_path,
        final_file_writer=sugar_file_writer,
        section_encoder=section_encoder,
        section_decoder=section_decoder,
        plugin_executor=plugin_executor,
        type_check=False,
    )


if __name__ == "__main__":
    app()

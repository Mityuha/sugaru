from pathlib import Path
from typing import Callable, Final, List, Type

import typer

from .file_loader import loader_by_extension
from .file_writer import stdout_writer_by_extension, writer_by_extension
from .interfaces import (
    FinalFileWriter,
    ObjectLoader,
    SectionDecoder,
    SectionEncoder,
    SugarFileLoader,
)
from .logging import logger
from .object_loader import SimpleObjectLoader
from .sugarator import sugarate
from .utils import decode_section, encode_section


STDOUT: Final[str] = "stdout"
AUTO: Final[str] = "auto"

app = typer.Typer()


def load_object_with_error(
    object_loader: ObjectLoader[Callable],
    *,
    obj_name: str,
    class_: Type[Callable],
    type_check: bool,
) -> Callable:
    objects: List[Callable] = object_loader(
        obj_name=obj_name,
        class_=class_,
        type_check=type_check,
    )
    if not objects:
        raise ImportError(f"Cannot load object '{obj_name}' by signature '{class_}'")

    return objects[0]


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
    type_check: bool = True,
) -> None:
    file_path: Path = Path(file)
    if not file_path.is_file():
        logger.warning(f"File '{file}' does not exist or is not a file")
        return

    object_loader: ObjectLoader = SimpleObjectLoader()
    if obj_loader != AUTO:
        object_loader = load_object_with_error(
            object_loader,
            obj_name=obj_loader,
            class_=ObjectLoader,
            type_check=type_check,
        )

    sugar_file_loader: SugarFileLoader
    if file_loader != AUTO:
        sugar_file_loader = load_object_with_error(
            object_loader,
            obj_name=file_loader,
            class_=SugarFileLoader,
            type_check=type_check,
        )
    else:
        ext: str = file_path.suffix
        if ext not in loader_by_extension:
            logger.warning(f"Cannot find plugin loader by extension '{ext}'")
            return

        sugar_file_loader = loader_by_extension[ext]

    sugar_file_writer: FinalFileWriter
    if file_writer != AUTO:
        sugar_file_writer = load_object_with_error(
            object_loader,
            obj_name=file_writer,
            class_=FinalFileWriter,
            type_check=type_check,
        )
    else:
        output_path: Path = Path(output)
        out_ext: str = output_path.suffix

        if out_ext not in writer_by_extension:
            logger.warning(f"Cannot find plugin writer by extension '{out_ext}'")
            return
        sugar_file_writer = writer_by_extension[out_ext]
        if output == STDOUT:
            sugar_file_writer = stdout_writer_by_extension[out_ext]

    section_encoder: SectionEncoder = encode_section
    section_decoder: SectionDecoder = decode_section

    if sec_encoder != AUTO:
        section_encoder = load_object_with_error(
            object_loader,
            obj_name=sec_encoder,
            class_=SectionEncoder,
            type_check=type_check,
        )

    if sec_decoder != AUTO:
        section_decoder = load_object_with_error(
            object_loader,
            obj_name=sec_decoder,
            class_=SectionDecoder,
            type_check=type_check,
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
        type_check=type_check,
    )


if __name__ == "__main__":
    app()

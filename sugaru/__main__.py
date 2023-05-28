from pathlib import Path
from typing import Final, List

import typer

from .file_loader import loader_by_extension
from .file_writer import writer_by_extension
from .interfaces import (
    FinalFileWriter,
    ObjectLoader,
    Plugin,
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


@app.command()
def main(
    file: str,
    plugin: List[str] = typer.Option(...),
    *,
    output: str = STDOUT,
    file_loader: str = AUTO,
    file_writer: str = AUTO,
    plug_loader: str = AUTO,
    type_check: bool = True,
) -> None:
    file_path: Path = Path(file)
    if not file_path.is_file():
        logger.warning(f"File '{file}' does not exist or is not file")
        return

    object_loader: ObjectLoader[Plugin] = SimpleObjectLoader()

    ext: str = file_path.suffix

    if ext not in loader_by_extension:
        logger.warning(f"Cannot find plugin loader by extension '{ext}'")
        return

    sugar_file_loader: SugarFileLoader = loader_by_extension[ext]

    if output != STDOUT:
        output_path: Path = Path(output)
        out_ext: str = output_path.suffix

        if out_ext not in writer_by_extension:
            logger.warning(f"Cannot find plugin writer by extension '{out_ext}'")
            return
        sugar_file_writer: FinalFileWriter = writer_by_extension[out_ext]

    section_encoder: SectionEncoder = encode_section
    section_decoder: SectionDecoder = decode_section

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

from pathlib import Path
from typing import Any, List, TypedDict

from pytest import fixture

from sugaru import (
    FinalFileWriter,
    ObjectLoader,
    SectionDecoder,
    SectionEncoder,
    SugarFileLoader,
    decode_section,
    encode_section,
)


class SugarateArgs(TypedDict):
    plugin_name_list: List[str]
    object_loader: ObjectLoader
    sugar_file_path: Path
    sugar_file_loader: SugarFileLoader
    final_file_path: Path
    final_file_writer: FinalFileWriter
    section_encoder: SectionEncoder
    section_decoder: SectionDecoder


@fixture
def sugarate_args(mocker: Any, faker: Any) -> SugarateArgs:
    return {
        "plugin_name_list": [faker.pystr() for _ in range(faker.pyint(max_value=10))],
        "object_loader": mocker.Mock(side_effect=[[mocker.Mock()]]),
        "sugar_file_loader": mocker.Mock(
            side_effect=[{faker.pystr(): faker.pydict() for _ in range(faker.pyint(max_value=20))}]
        ),
        "final_file_writer": mocker.Mock(),
        "sugar_file_path": Path(faker.pystr()),
        "final_file_path": Path(faker.pystr()),
        "section_encoder": encode_section,
        "section_decoder": decode_section,
    }

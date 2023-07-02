import json
import tempfile
from pathlib import Path
from typing import Any

from sugaru.file_writer import json_to_stdout, simple_json_writer


def test_simple_json_writer(faker: Any) -> None:
    dict_content: Any = faker.pydict(value_types=[int, str])

    with tempfile.NamedTemporaryFile(suffix=".yaml") as json_path:
        path: Path = Path(json_path.name)

        simple_json_writer(path=path, content=dict_content)

        got_content: dict = json.load(json_path)

        assert got_content == dict_content


def test_json_to_stdout(faker: Any) -> None:
    dict_content: Any = faker.pydict(value_types=[int, str])
    json_to_stdout(dict_content)

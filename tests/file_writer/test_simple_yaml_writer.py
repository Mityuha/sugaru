import tempfile
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from sugaru.file_writer import simple_yaml_writer, yaml_to_stdout


def test_simple_yaml_writer(faker: Any) -> None:
    dict_content: Any = faker.pydict(value_types=[str, int])

    with tempfile.NamedTemporaryFile(suffix=".yaml") as yml_path:
        path: Path = Path(yml_path.name)

        simple_yaml_writer(path=path, content=dict_content)

        got_content: dict = yaml.safe_load(yml_path)

        assert got_content == dict_content


def test_yaml_to_stdout(faker: Any) -> None:
    dict_content: Any = faker.pydict(value_types=[str, int])
    yaml_to_stdout(dict_content)

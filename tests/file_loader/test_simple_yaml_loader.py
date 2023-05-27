import tempfile
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from sugaru.file_loader import simple_yaml_loader
from sugaru.file_loader.simple_yaml.loader import Ref


def test_simple_yaml_loader(mocker: Any) -> None:
    yaml_content: str = """
include:
  - project: "some/project/path"
    ref: "master"
    file:
        - "file/one.yml"
        - "file/two.yml"

stages:
    - "stage1"
    - "stage2"

variables:
    VAR1: "value1"
    VAR2: "value2"

some-job-1:
    stage: "stage1"
    image: !reference [.some_section, some_image]
    cache: &cache_anchor
        key:
            files:
                - cache_file
            prefix: "some_prefix"
        path:
            - some-path

    rules:
        - if: 'some condition'
          allow_failure: true
    """

    def eq_method(self: Ref, other: Ref) -> bool:
        return self._values == other._values

    mocker.patch.object(Ref, "__eq__", eq_method)

    dict_content: dict = yaml.safe_load(yaml_content)

    with tempfile.NamedTemporaryFile(suffix=".yml") as yml_path:
        path: Path = Path(yml_path.name)
        with path.open("w") as f:
            f.write(yaml_content)

        sections: dict = simple_yaml_loader(path)
        assert sections == dict_content

import json
import sys
import tempfile
from functools import partial
from pathlib import Path
from random import choice
from typing import Any, Callable, Iterator

import pytest
import yaml  # type: ignore
from typer.testing import CliRunner

from sugaru.__main__ import app


@pytest.fixture
def tmp_sys_path() -> Iterator[str]:
    paths: list[str] = [p for p in sys.path if p.endswith("site-packages")]
    base_path: str = choice(paths)
    with tempfile.NamedTemporaryFile(suffix=".py", dir=base_path) as py_path:
        yield py_path.name


@pytest.fixture
def dummy_plugin_name(tmp_sys_path: str) -> Iterator[str]:
    dict_import: str = ""
    dict_type: str = "dict"

    if sys.version_info < (3, 9):
        dict_import = "from typing import Dict"
        dict_type = "Dict"

    content: str = f'''
{dict_import}
from sugaru import Section
def dummy(section: Section, section_name: str, sections: {dict_type}[str, Section]) -> Section:
    return section
    '''
    path: Path = Path(tmp_sys_path)
    with path.open("w", encoding="utf-8") as f:
        f.write(content)

    yield path.stem


@pytest.fixture
def output_yaml() -> Iterator[str]:
    with tempfile.NamedTemporaryFile(suffix=".yaml") as f:
        yield f.name


@pytest.fixture
def random_yaml(faker: Any) -> Iterator[str]:
    json_obj: str = faker.json()
    with tempfile.NamedTemporaryFile(suffix=".yml") as f:
        with open(f.name, "w") as yaml_f:
            yaml.dump(json.loads(json_obj), yaml_f)
        yield f.name


@pytest.fixture
def run_app() -> Iterator[Callable]:
    runner = CliRunner()
    yield partial(runner.invoke, app, catch_exceptions=False)

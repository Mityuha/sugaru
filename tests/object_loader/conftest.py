import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from random import choice
from typing import Iterator, List

from pytest import fixture


@dataclass
class PluginPath:
    file_path: str
    py_path: str


@dataclass
class PluginContent:
    content: str
    plugin_names: List[str]
    object_names: List[str]


@fixture(scope="module")
def plugin_content() -> PluginContent:
    plugin_num: int = 5
    plugin_name: str = "MultiPluginTest"

    dict_import: str = ""
    dict_type: str = "dict"

    if sys.version_info < (3, 9):
        dict_import = "from typing import Dict"
        dict_type = "Dict"

    plugin_content: str = "\n\n".join(
        f"""
{dict_import}
from sugaru import Section, SecName
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, section: Section, section_name: str, sections: {dict_type}[str, Section]) -> Section:
        return {{}}

def {plugin_name.lower()}{i}(*, section: Section, section_name: SecName, sections: {dict_type}[str, Section]) -> Section:
    return {{}}

def some_custom_func{i}(x: int) -> int:
    return x
    """
        for i in range(plugin_num)
    )

    plugin_names: List[str] = [f"{plugin_name}{i}" for i in range(plugin_num)] + [
        f"{plugin_name.lower()}{i}" for i in range(plugin_num)
    ]

    return PluginContent(
        content=plugin_content,
        plugin_names=plugin_names,
        object_names=plugin_names + [f"some_custom_func{i}" for i in range(plugin_num)],
    )


@fixture
def plugin_path(plugin_content: PluginContent) -> Iterator[PluginPath]:
    paths: list[str] = [p for p in sys.path if p.endswith("site-packages")]
    base_path: str = choice(paths)
    print(sys.path, paths, base_path)
    with tempfile.TemporaryDirectory(dir=base_path) as package_path:
        with open(f"{package_path}/__init__.py", "w"):
            ...
        with tempfile.NamedTemporaryFile(suffix=".py", dir=package_path) as py_path:
            with open(py_path.name, "w") as f:
                f.write(plugin_content.content)

            dir_name: str = package_path.split("/")[-1]
            file_name: str = Path(py_path.name).stem
            yield PluginPath(file_path=py_path.name, py_path=f"{dir_name}.{file_name}")

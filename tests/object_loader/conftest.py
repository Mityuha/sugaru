import sys
import tempfile
from dataclasses import dataclass
from importlib import invalidate_caches
from pathlib import Path
from random import choice
from typing import Iterator, List

from faker import Faker
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


def prepare_content(template: str, plugin_name: str) -> PluginContent:
    plugin_num: int = Faker().pyint(max_value=10)
    class_tmpl, func_tmpl = template.split("\n\n")

    plugin_content: str = "\n\n".join(
        [class_tmpl.format(plugin_name=plugin_name, i=i) for i in range(plugin_num)]
        + [func_tmpl.format(plugin_name=plugin_name.lower(), i=i) for i in range(plugin_num)]
    )

    plugin_names: List[str] = [f"{plugin_name}{i}" for i in range(plugin_num)] + [
        f"{plugin_name.lower()}{i}" for i in range(plugin_num)
    ]
    return PluginContent(
        content=plugin_content,
        plugin_names=plugin_names,
        object_names=plugin_names,
    )


@fixture(scope="module")
def full_plugins() -> PluginContent:
    template: str = """
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, section: Section, section_name: str, sections: Mapping[str, Section]) -> Section:
        return {{}}

def {plugin_name}{i}(*, section: Section, section_name: SecName, sections: Mapping[str, Section]) -> Section:
    return {{}}
    """
    return prepare_content(template, "FullPlugin")


@fixture(scope="module")
def only_section_plugins() -> PluginContent:
    template: str = """
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, section: Section) -> Section:
        return {{}}

def {plugin_name}{i}(*, section: Section) -> Section:
    return {{}}
    """
    return prepare_content(template, "OnlySectionPlugin")


@fixture(scope="module")
def only_section_name_plugins() -> PluginContent:
    template: str = """
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, section_name: str) -> Section:
        return {{}}

def {plugin_name}{i}(*, section_name: str) -> Section:
    return {{}}
    """
    return prepare_content(template, "OnlySectionNamePlugin")


@fixture(scope="module")
def only_section_map_plugins() -> PluginContent:
    template: str = """
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, sections: Mapping[str, Section]) -> Section:
        return {{}}

def {plugin_name}{i}(*, sections: Mapping[str, Section]) -> Section:
    return {{}}
    """
    return prepare_content(template, "OnlySectionMapPlugin")


@fixture(scope="module")
def section_with_name_plugins() -> PluginContent:
    template: str = """
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, section: Section, section_name: str) -> Section:
        return {{}}

def {plugin_name}{i}(*, section: Section, section_name: str) -> Section:
    return {{}}
    """
    return prepare_content(template, "SectionWithNamePlugin")


@fixture(scope="module")
def section_map_with_name_plugins() -> PluginContent:
    template: str = """
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, sections: Mapping[str, Section], section_name: str) -> Section:
        return {{}}

def {plugin_name}{i}(*, sections: Mapping[str, Section], section_name: str) -> Section:
    return {{}}
    """
    return prepare_content(template, "SectionMapWithNamePlugin")


@fixture(scope="module")
def section_map_with_section_plugins() -> PluginContent:
    template: str = """
class {plugin_name}{i}:
    @staticmethod
    def __call__(*, sections: Mapping[str, Section], section: Section) -> Section:
        return {{}}

def {plugin_name}{i}(*, sections: Mapping[str, Section], section: Section) -> Section:
    return {{}}
    """
    return prepare_content(template, "SectionMapWithSectionPlugin")


@fixture(scope="module")
def plugin_content(
    *,
    full_plugins: PluginContent,
    only_section_plugins: PluginContent,
    only_section_name_plugins: PluginContent,
    only_section_map_plugins: PluginContent,
    section_with_name_plugins: PluginContent,
    section_map_with_name_plugins: PluginContent,
    section_map_with_section_plugins: PluginContent,
) -> PluginContent:
    imports: str = "\n".join(
        [
            "from typing import Dict, Mapping",
            "from sugaru import Section, SecName",
        ]
    )

    bad_plugin: str = """
def some_custom_func(x: int) -> int:
    return x
    """

    content: List[str] = [imports, bad_plugin]
    names: List[str] = []
    object_names: List[str] = ["some_custom_func"]

    for plugin in (
        full_plugins,
        only_section_plugins,
        only_section_name_plugins,
        only_section_map_plugins,
        section_with_name_plugins,
        section_map_with_name_plugins,
        section_map_with_section_plugins,
    ):
        content.append(plugin.content)
        names.extend(plugin.plugin_names)
        object_names.extend(plugin.object_names)

    return PluginContent(
        content="\n\n".join(content),
        plugin_names=names,
        object_names=object_names,
    )


@fixture
def plugin_path(plugin_content: PluginContent) -> Iterator[PluginPath]:
    paths: list[str] = [p for p in sys.path if p.endswith("site-packages")]
    base_path: str = choice(paths)
    with tempfile.TemporaryDirectory(dir=base_path) as package_path:
        with open(f"{package_path}/__init__.py", "w"):
            ...
        with tempfile.NamedTemporaryFile(suffix=".py", dir=package_path) as py_path:
            with open(py_path.name, "w") as f:
                f.write(plugin_content.content)

            invalidate_caches()
            dir_name: str = package_path.split("/")[-1]
            file_name: str = Path(py_path.name).stem
            yield PluginPath(file_path=py_path.name, py_path=f"{dir_name}.{file_name}")

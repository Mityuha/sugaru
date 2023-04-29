from pathlib import Path
from typing import Any, List, TypedDict

from pytest import fixture

from sugaru import FinalFileWriter, PluginLoader, PluginNamesFetcher, SugarFileLoader


class SugarateArgs(TypedDict):
    plugin_name_list: List[str]
    plugin_names_fetcher: PluginNamesFetcher
    plugin_loader: PluginLoader
    sugar_file_path: Path
    sugar_file_loader: SugarFileLoader
    final_file_path: Path
    final_file_writer: FinalFileWriter


@fixture
def sugarate_args(mocker: Any, faker: Any) -> SugarateArgs:
    return {
        "plugin_name_list": [faker.pystr() for _ in range(faker.pyint(max_value=10))],
        "plugin_names_fetcher": mocker.Mock(
            side_effect=[
                [faker.pystr() for _ in range(faker.pyint(max_value=10))],
            ]
        ),
        "plugin_loader": mocker.Mock(side_effect=[[mocker.Mock()]]),
        "sugar_file_loader": mocker.Mock(side_effect={}),
        "final_file_writer": mocker.Mock(),
        "sugar_file_path": Path(faker.pystr()),
        "final_file_path": Path(faker.pystr()),
    }

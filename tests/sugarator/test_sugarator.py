from typing import Any

from sugaru import sugarate
from . import SugarateArgs


def test_sugarate_no_plugins_to_fetch(sugarate_args: SugarateArgs, mocker: Any) -> None:
    sugarate_args["plugin_name_list"] = []
    fetcher: Any = sugarate_args["plugin_names_fetcher"]
    fetcher.configure_mock(side_effect=[[]])

    sugarate(**sugarate_args)

    assert fetcher.mock_calls == [mocker.call()]
    assert sugarate_args["plugin_loader"].mock_calls == []  # type: ignore
    assert sugarate_args["sugar_file_loader"].mock_calls == []  # type: ignore
    assert sugarate_args["final_file_writer"].mock_calls == []  # type: ignore

from typing import Any, List

from sugaru import sugarate
from . import SugarateArgs


def test_sugarate_no_plugins_to_fetch(sugarate_args: SugarateArgs, mocker: Any) -> None:
    sugarate_args["plugin_name_list"] = []

    sugarate(**sugarate_args)

    assert sugarate_args["plugin_loader"].mock_calls == []  # type: ignore
    assert sugarate_args["sugar_file_loader"].mock_calls == []  # type: ignore
    assert sugarate_args["final_file_writer"].mock_calls == []  # type: ignore


def test_sugarate_plugins_not_found(sugarate_args: SugarateArgs, mocker: Any) -> None:
    plugins: List[str] = sugarate_args["plugin_name_list"]
    sugarate_args["plugin_loader"].configure_mock(side_effect=[None for _ in range(len(plugins))])  # type: ignore
    sugarate(**sugarate_args)

    assert sugarate_args["plugin_loader"].mock_calls == [mocker.call(pname) for pname in plugins]  # type: ignore
    assert sugarate_args["sugar_file_loader"].mock_calls == []  # type: ignore
    assert sugarate_args["final_file_writer"].mock_calls == []  # type: ignore


def test_sugarate_run_plugins_against_sections(
    sugarate_args: SugarateArgs,
    mocker: Any,
) -> None:
    plugins: List[str] = sugarate_args["plugin_name_list"]
    sugarate_args["plugin_loader"].configure_mock(  # type: ignore
        side_effect=[
            [lambda section, section_name, **_kwargs: section] for _ in range(len(plugins))
        ]
    )

    sugarate(**sugarate_args)

    assert sugarate_args["plugin_loader"].mock_calls == [mocker.call(pname) for pname in plugins]  # type: ignore
    assert sugarate_args["sugar_file_loader"].mock_calls == [mocker.call(sugarate_args["sugar_file_path"])]  # type: ignore
    assert sugarate_args["final_file_writer"].mock_calls == [  # type: ignore
        mocker.call(path=sugarate_args["final_file_path"], content=mocker.ANY)
    ]

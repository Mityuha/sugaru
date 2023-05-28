from typing import Callable

import yaml  # type: ignore


def test_yaml_dummy_plugin(
    random_yaml: str, output_yaml: str, dummy_plugin_name: str, run_app: Callable
) -> None:
    result = run_app([random_yaml, '--plugin', dummy_plugin_name, "--output", output_yaml])

    print(result.stdout)
    assert result.exit_code == 0

    with open(random_yaml) as in_file, open(output_yaml) as out_file:
        exp: dict = yaml.safe_load(in_file)
        got: dict = yaml.safe_load(out_file)

    assert exp == got

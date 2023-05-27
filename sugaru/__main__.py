from typing import Final, List

import typer


STDOUT: Final[str] = "stdout"
AUTO: Final[str] = "auto"


def main(
    file: str,
    plugin: List[str] = typer.Option(...),
    *,
    output: str = STDOUT,
    file_loader: str = AUTO,
    file_writer: str = AUTO,
    plugin_loader: str = AUTO,
    type_check: bool = True,
) -> None:
    print("file got", file, plugin)


if __name__ == "__main__":
    typer.run(main)

from pathlib import Path
from typing import Any

# pip install toml
import toml


def toml_loader(path: Path) -> Any:
    return toml.load(path)


def toml_output(path: Path, content: Any) -> None:
    print(toml.dumps(content))

import json
import tempfile
from pathlib import Path
from typing import Any

from sugaru import JSON, simple_json_loader


def test_simple_json_loader(faker: Any) -> None:
    json_content: str = faker.json()
    dict_content: dict = json.loads(json_content)

    with tempfile.NamedTemporaryFile(suffix=".yml") as json_path:
        path: Path = Path(json_path.name)
        with path.open("w") as f:
            f.write(json_content)

        sections: JSON = simple_json_loader(path)
        assert sections == dict_content

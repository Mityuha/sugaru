from typing import Dict, Final

from ..interfaces import FinalFileWriter
from .simple_json import to_stdout as json_to_stdout
from .simple_json import writer as simple_json_writer
from .simple_yaml import to_stdout as yaml_to_stdout
from .simple_yaml import writer as simple_yaml_writer


writer_by_extension: Final[Dict[str, FinalFileWriter]] = {
    ".yaml": simple_yaml_writer,
    ".yml": simple_yaml_writer,
    ".json": simple_json_writer,
}

output_writer_by_extension: Final[Dict[str, FinalFileWriter]] = {}

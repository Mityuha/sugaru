from typing import Any, Dict, List


def generate_stages(section_name: str, section: Any, sections: Dict[str, Any]) -> List[str]:
    if section_name != "stages":
        return section

    known_stages: Dict[str, str] = {"python-tests": "tests"}
    try:
        return [known_stages[stage] for stage in sections if stage != "stages"]
    except KeyError as unknown_stage:
        raise ValueError(f"Unknown stage: {unknown_stage}") from None


def generate_tests(section_name: str, section: Any) -> Dict[str, Any]:
    if section_name != "python-tests":
        return section

    py_image: str = section
    return {
        "stage": "tests",
        "image": py_image,
        "before_script": ["poetry install"],
        "script": ["poetry run pytest"],
    }

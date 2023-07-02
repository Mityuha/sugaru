from typing import Dict

from ..types import JSON, SecName, Section


__all__ = ["decode_section", "encode_section"]


def encode_section(content: JSON) -> Dict[SecName, Section]:
    if isinstance(content, list):
        return {str(i): item for i, item in enumerate(content)}

    if isinstance(content, (str, int, float, type(None), bool)):
        return {"": content}

    assert isinstance(content, dict)
    return content


def decode_section(sections: Dict[SecName, Section], *, origin: JSON) -> JSON:
    if isinstance(origin, list):
        return [item for item in sections.values()]

    if isinstance(origin, (str, int, float, type(None), bool)):
        return sections[""]

    assert isinstance(origin, dict)
    return sections

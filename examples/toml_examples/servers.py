from typing import Any, Dict


def add_servers(section_name: str, section: Dict[str, Any]) -> Dict[str, Any]:
    if section_name != "servers":
        return section

    if section.pop("alpha", False):
        section["servers.alpha"] = {
            "ip": "10.0.0.1",
            "dc": "eqdc10",
        }

    if section.pop("beta", False):
        section["servers.beta"] = {
            "ip": "10.0.0.2",
            "dc": "eqdc10",
        }

    return section

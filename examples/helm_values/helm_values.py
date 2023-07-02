from typing import Dict, Union


def replica_count(section_name: str, section: str) -> Union[str, int]:
    if section_name != "replicaCount" or not isinstance(section, str):
        return section

    replicas: Dict[str, int] = {"minimum": 1, "maximum": 3}
    return replicas[section]


def image(section_name: str, section: str) -> Union[str, Dict]:
    if section_name != "image" or not isinstance(section, str):
        return section

    if section != "nginx_latest":
        raise ValueError("Only 'nginx_latest' value available")

    return {
        "repository": "nginx",
        "tag": "latest",
        "pullPolicy": "IfNotPresent",
    }


def service(section_name: str, section: str) -> Union[str, Dict]:
    if section_name != "service" or not isinstance(section, str):
        return section

    if not section.startswith("nginx_"):
        raise ValueError("Section 'service' should be template 'nginx_{port}'")

    port: int = int(section.split("_")[1])

    return {
        "name": "nginx",
        "type": "ClusterIP",
        "externalPort": port,
        "internalPort": port,
    }

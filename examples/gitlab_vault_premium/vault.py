from typing import Any, Dict, List, Mapping, cast

from typing_extensions import NotRequired, TypedDict

from sugaru import Section


class VaultSection(TypedDict):
    id_tokens: NotRequired[Dict[str, Any]]
    secrets: NotRequired[Dict[str, Any]]
    variables: Dict[str, Any]
    script: List[Any]


def vault_plugin(
    section_name: str, section: VaultSection, sections: Mapping[str, Section]
) -> Section:
    if not isinstance(section, dict):
        return section

    if "id_tokens" not in section:
        return cast(Section, section)

    tokens_aud: List[str] = [token["aud"] for token in section.pop("id_tokens").values()]

    secrets: List = [
        (
            var_name,
            value["vault"],
            value["token"],
        )
        for var_name, value in section.pop("secrets").items()
    ]

    variables: Dict = section.get("variables", {})

    variables["VAULT_ADDRESS"] = tokens_aud[0]

    # save only last variable
    for secret in secrets:
        secret_path, *secret_engine = secret[1].split("@")
        if secret_engine:
            secret_engine = secret_engine[0]

        variables["VAULT_VAR_NAME"] = secret[0]
        variables["VAULT_SECRET_ENGINE"] = secret_engine
        variables["VAULT_SECRET_PATH"] = secret_path
        variables["VAULT_TOKEN"] = secret[2]

    section["variables"] = variables

    script: List = section.get("script", [])
    script.insert(0, f"export {variables['VAULT_VAR_NAME']}=$(./some_script_to_fetch_var.sh)")
    section["script"] = script

    return cast(Section, section)

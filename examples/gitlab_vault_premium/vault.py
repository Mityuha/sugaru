from typing import Any, Dict, List

from typing_extensions import NotRequired, TypedDict


class VaultSection(TypedDict):
    id_tokens: NotRequired[Dict[str, Any]]
    secrets: NotRequired[Dict[str, Any]]
    variables: Dict[str, Any]
    script: List[Any]


def vault_plugin(section: VaultSection) -> Any:
    '''https://docs.gitlab.com/ee/ci/secrets/#use-vault-secrets-in-a-ci-job
      job_using_vault:
    id_tokens:
      VAULT_ID_TOKEN:
        aud: https://gitlab.com
    secrets:
      DATABASE_PASSWORD:
        vault: production/db/password@ops  # translates to secret `ops/data/production/db`, field `password`
        token: $VAULT_ID_TOKEN
    '''
    if not isinstance(section, dict) or "id_tokens" not in section:
        return section

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

    return section

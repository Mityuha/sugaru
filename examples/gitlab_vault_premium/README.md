# Gitlab vault premium plugin
It might happen that it's your organization that has Gitlab as CI/CD system.      
It also might happen that Gitlab tier is not premium.    
But what if you want to have some features that Gitlab Premium has?        
Or even more: what if you want to have some extra special `.gitlab-ci.yml` syntax dedicated to your team needs.   
Let's consider the case of non-premium Gitlab when you want to get [Vault premium syntax](https://docs.gitlab.com/ee/ci/secrets/#use-vault-secrets-in-a-ci-job).    
Let's suppose that your team has some script that's able to fetch variable values from Vault storage.    
Call such a script `some_script_to_fetch_var.sh`.    
What input data does this script need?  
- VAULT_ADDRESS -- the URI of the Vault
- VAULT_TOKEN -- authentication token for Vault
- VAULT_SECRET_ENGINE -- Vault secret engine name
- VAULT_SECRET_PATH -- Vault path to variables to fetch. It's located inside ${VAULT_SECRET_ENGINE}
- VAULT_VAR_NAME -- the name of the variable to fetch

So if you thorough specify all variables listed above and call the `some_script_to_fetch_var.sh` script you get the value of the ${VAULT_VAR_NAME} variable stored inside Vault.   
## Expected input
It doesn't matter what syntax you're going to use. It can be your specially invented syntax or something like this.   
But it this case we simply borrow the syntax that Gitlab Premium has.    
So the syntax is just right from [the documentation](https://docs.gitlab.com/ee/ci/secrets/#use-vault-secrets-in-a-ci-job):
```yaml
stages:
    - "vault_stage"

job_using_vault:
  stage: "vault_stage"
  id_tokens:
    VAULT_ID_TOKEN:  # <<< should be converted to ${VAULT_TOKEN}
      aud: https://your-gitlab.com  # <<< shourd be converted to ${VAULT_ADDRESS}
  secrets:
    DATABASE_PASSWORD:  # <<< ${VAULT_VAR_NAME}
      vault: production/db/password@ops  # <<< translates to secret `ops/data/production/db`, field `password`
      token: $VAULT_ID_TOKEN

  script:
    - echo "Use ${DATABASE_PASSWORD} here"
```

## Expected output
We are expecting that all script's variables are exported.    
We are also expecting that ${VAULT_VAR_NAME} variable are exported as well with the correct value.   
The correct value of the variable is getting using the script `some_script_to_fetch_var.sh`.
```yaml
stages:
- vault_stage

job_using_vault:
  stage: vault_stage
  variables:
    VAULT_ADDRESS: https://your-gitlab.com
    VAULT_SECRET_ENGINE: ops
    VAULT_SECRET_PATH: production/db/password
    VAULT_TOKEN: $VAULT_ID_TOKEN
    VAULT_VAR_NAME: DATABASE_PASSWORD
  script:
  - export DATABASE_PASSWORD=$(./some_script_to_fetch_var.sh)
  - echo "Use ${DATABASE_PASSWORD} here"
```

## Run it
For getting such a transformation we have to write the plugin. Let's call it `vault` (vault.py).   
To run this `vault` plugin type:
```bash
$ python3 -m sugaru .your-gitlab-ci.yml --plugin vault
```
That's it. You'll see the expected output on your screen. 

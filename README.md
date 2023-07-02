
<p align="center">
  <a href="https://pypi.org/project/sugaru/"><img width="300px" src="https://github.com/Mityuha/sugaru/assets/17745407/c4429d72-8e53-49d5-97c2-f6421c6a320c" alt='sugaru'></a>
</p>
<p align="center">
    <em>🍭 Your own syntax you've always been dreaming of. 🍭</em>
</p>

---

# Sugaru

Sugaru is a lightweight completely customizable plugin system,
that gives you an opportunity to do things like:

* Writing files followed your own syntax.
* Translating such files to ones with any other syntax.
* Any custom user-defined replacements (e.g. templates' replacements with environment variables).
* Converting files from one format to another (yaml --> json, toml --> ini, etc).
* Any other fascinating features you can imagine not listed above.

## Requirements

Python 3.7+

## Installation

```shell
$ pip3 install sugaru
```

## Quickstart
It's better to see something once than to read documentation a thousand times. Let's follow this principle.    
You are a kind of DevOps engineer. You write CI files every day. That's why you've learnt by heart some CI stages: literally, line-by-line.   
One day you've feded up with copy-pasting/writing complete stages into the new project. And you have decided to reduce time and effort to write the same stage the hundredth time.   
You took a close look to your stage once again:
```yaml
stages:
  - tests

pytest:
  stage: "tests"
  image: "python:3.12.0"
  before_script:
    - poetry install
  script:
    - poetry run pytest
```
And came up with idea to simply remove it. Indeed, the presence of `python-tests` stage means the same stage code every time. Why not just generate such a stage then? You ended up with the syntax like:
```yaml
stages: ""
python-tests: "python:3.12.0"
```
That's it! Looks good, doesn't it?     
To translate `python-tests` stage to `tests` one let's write a couple of plugins that will do the job.    
The first one will generate `stages` section:
```python
from typing import Any, Dict, List


def generate_stages(section_name: str, section: Any, sections: Dict[str, Any]) -> List[str]:
    if section_name != "stages":
        return section

    known_stages: Dict[str, str] = {"python-tests": "tests"}
    try:
        return [known_stages[stage] for stage in sections if stage != "stages"]
    except KeyError as unknown_stage:
        raise ValueError(f"Unknown stage: {unknown_stage}") from None
```
The second plugin with generate `python-tests` section:
```python
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
```
Let's put our plugins into the file called `python_tests.py`. And put our awesome yml syntax into the file called `.my-gitlab-ci.yml`.   
To make it work simply type:
```bash
$ python3 -m sugaru .my-gitlab-ci.yml --plugin python_tests
```
That's it. You will see the correct `.gitlab-ci.yml` syntax output on your screen.






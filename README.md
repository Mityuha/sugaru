
<p align="center">
  <a href="https://pypi.org/project/sugaru/"><img width="300px" src="https://github.com/Mityuha/sugaru/assets/17745407/4b25b429-620e-4718-8643-70b11cde0065" alt='sugaru'></a>
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

## Table of contents
   * [Quickstart](#quickstart)
   * [How it actually works](#how-it-actually-works)
   * [Preparations under the hood](#preparations-under-the-hood)
   * [How objects are loaded](#how-objects-are-loaded)
   * [Examples](#examples)
   * [Dependencies](#dependencies)
   * [Changelog](#changelog)

## Quickstart
It's better to see something once than to read documentation a thousand times. Let's follow this principle.    
You are a kind of DevOps engineer. You write CI files every day. That's why you've learnt by heart some CI stages: literally, line-by-line.   
One day you've fed up with copy-pasting/writing complete stages into the new project. And you have decided to reduce time and effort to write the same stage the hundredth time.   
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
And came up with idea to simply remove it. Indeed, the presence of some `python-tests` stage can mean the same stage's code every time. Why not just generate such a stage then? You ended up with the syntax like:
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
The second plugin will generate `python-tests` section:
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
<p align="left">
  <img width="400px" src="https://github.com/Mityuha/sugaru/assets/17745407/b47f9353-1f95-4407-83fb-13fb18abfa91" alt='how-it-works-no-detail'>
</p>
This picture illustrates how sugaru works in a nutshell.

## How it actually works
There are some classes under the hood that work as a pipeline:    
<p align="left">
  <img width="400px" src="https://github.com/Mityuha/sugaru/assets/17745407/c94cda75-b50c-48d8-827b-62d50e9d94f3" alt='how-it-works'>
</p>
There is a file path as an entry point parameter (e.g. path to `.my-gitlab-ci.yml`). Then the output of every component is the input of the next component.

* File Loader  
  * Output: file content as any JSON type
* Section Encoder
  * Output: sections, i.e. mapping section-name: section-content.
* Plugin Executor
  * Output: sections after every plugin execution
* Section Decoder
  * Output: file content as any JSON type
* File Writer
  * Output: the file with the content (including stdout)

There is also an interesting component called Object Loader. We'll discuss it later.

## Preparations under the hood
There is the default implementation for every component listed above.    
Instead of using default components, you can define your own ones.    
If you do so, such components are loaded by Object Loader component.    

<p align="left">
  <img width="600px" src="https://github.com/Mityuha/sugaru/assets/17745407/f1c97b38-a469-4d72-900a-c02eff81f956" alt='components-loading'>
</p>

And what about the Object Loader component itself?    
Actually, you can even implement a custom Object Loader component. Such the custom Object Loader will be loaded by default Object Loader first and then will *replace* the default one.

## How objects are loaded
All custom defined objects -- including user plugins -- are loaded by interfaces.    
To implement your own component you have to implement the interface dedicated to it.  
For example, to implement custom Section Encoder you have to implement the following interface:
```python
class SectionEncoder(Protocol):
    def __call__(self, content: JSON) -> Dict[SecName, Section]:
        ...
```
The only exception is user Plugin. A plugin interface is defined as
```python
class Plugin(Protocol):
    def __call__(
        self,
        *,
        section: Section,
        section_name: str,
        sections: Mapping[SecName, Section],
    ) -> Section:
        ...
```
To implement a plugin you should define *any* combination of interfaces' parameters. For example the following implementation also fits:
```python
def empty_section(section_name: str) -> Any:
    print(section_name)
    return {}
```
The last thing you should known about interface's implementation is that type hints are not validated by sugaru (yet). It's up to you to use type hints for your own purposes.      
Take a closer look to `interfaces.py` file for more interfaces' detail.

## Examples
You will find more examples with detail explanations inside [examples](https://github.com/Mityuha/sugaru/tree/main/examples) folder.

## Dependencies

The only sugaru's dependency is [typer](https://typer.tiangolo.com/). Typer makes sugaru more convenient to use.   
You can also install [loguru](https://loguru.readthedocs.io/en/stable/) for more beautiful logs.

## Changelog
You can see the release history here: https://github.com/Mityuha/sugaru/releases/

---

<p align="center"><i>Sugaru is <a href="https://github.com/Mityuha/sugaru/blob/main/LICENSE">MIT licensed</a> code.</p>

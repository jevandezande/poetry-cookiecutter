# Poetry Cookiecutter
[![License](https://img.shields.io/github/license/jevandezande/poetry-cookiecutter)](https://github.com/jevandezande/poetry-cookiecutter/blob/master/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jevandezande/poetry-cookiecutter/test.yml?branch=master&logo=github-actions)](https://github.com/jevandezande/poetry-cookiecutter/actions/)
[![Codecov](https://img.shields.io/codecov/c/github/jevandezande/poetry-cookiecutter)](https://app.codecov.io/github/jevandezande/poetry-cookiecutter)

[Cookiecutter](https://github.com/audreyr/cookiecutter) for setting up [poetry](https://python-poetry.org/) projects with all of the below features.

## Features
- Packaging with [poetry](https://python-poetry.org/)
- Formatting and linting with [ruff](https://github.com/charliermarsh/ruff)
- Static typing with [mypy](http://mypy-lang.org/)
- Testing with [pytest](https://docs.pytest.org/en/latest/)
- Git hooks that run all the above with [pre-commit](https://pre-commit.com/)
- Continuous Integration with [GitHub Actions](https://github.com/features/actions)
- Code coverage with [Codecov](https://docs.codecov.com/docs)


## Setup
While all of the steps are automated, you will need to install `poetry`.
Additionally, `pipx` is recommended for installing any command line tools.

```sh
python3 -m pip install pipx
pipx ensurepath

# Install poetry and cookiecutter using pipx
pipx install poetry cookiecutter

# Use cookiecutter to create project from this template
pipx run cookiecutter gh:jevandezande/poetry-cookiecutter
```

The cookiecutter will automagically
- Generate a project with the input configuration
- Initialise git
- Install dependencies
- Setup pre-commit and pre-push hooks
- Make initial commit
- Setup remote on GitHub (optional)


## Recommendations
Make a config file (see [template_config.yml](template_config.yml)) with
default settings and save it as a `.cookiecutterrc` or use it directly via:
`--config-file cookiecutter.yml`

Install [act](https://github.com/nektos/act) to run GitHub Actions locally.

Read [notes](notes.md) for more tips.

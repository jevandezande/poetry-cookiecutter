# {{cookiecutter.project_name}}

{% if cookiecutter.license == "None" %}![License](https://img.shields.io/badge/license-None-black){% else %}[![License](https://img.shields.io/github/license/{{cookiecutter.github_username}}/{{cookiecutter.package_name}})]({{cookiecutter.project_url}}/blob/master/LICENSE){% endif %}
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/{{cookiecutter.github_username}}/{{cookiecutter.package_name}}/test.yml?branch=master&logo=github-actions)]({{cookiecutter.project_url}}/actions/)
[![Codecov](https://img.shields.io/codecov/c/github/{{cookiecutter.github_username}}/{{cookiecutter.package_name}})](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.package_name}})


## Credits
This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [jevandezande/poetry-cookiecutter](https://github.com/jevandezande/poetry-cookiecutter) project template.

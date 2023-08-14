from __future__ import annotations

import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from subprocess import check_call
from typing import Literal

logger = logging.Logger("post_gen_project_logger")
logger.setLevel(logging.INFO)


PROTOCOL = Literal["git", "https"]


def call(*inputs: str) -> None:
    """
    Call shell commands.
    Warning: strings with spaces are not yet supported.
    """
    for input in inputs:
        logger.debug(f"Calling: {input}")
        check_call(input.split())


def set_python_version() -> None:
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    logger.info(f"Settting {python_version=}")
    if sys.version_info.minor < 9:
        logger.warn(f"{python_version=} should be upgraded to the latest avaiable python version.")

    file_names = [
        ".github/workflows/test.yml",
        "pyproject.toml",
    ]

    for file_name in file_names:
        with open(file_name) as f:
            contents = f.read().replace("{python_version}", python_version)
        with open(file_name, "w") as f:
            f.write(contents)


def set_license(license: str | None = "MIT") -> None:
    if not license or license == "None":
        logger.debug("No license set")
        return

    license = license.lower()
    licenses = [lic.name for lic in Path("licenses").iterdir()]
    if license not in licenses:
        raise ValueError(f"{license=} is not available yet. Please select from:\n{licenses=}")

    shutil.copy(f"licenses/{license}", "LICENSE")

    with open("LICENSE") as f:
        contents = f.read().replace("{year}", f"{datetime.now().year}")
        contents = contents.replace("{author_name}", "{{cookiecutter.author_name}}")
    with open("LICENSE", "w") as f:
        f.write(contents)

    logger.debug(f"Set {license=}")


def remove_license_dir() -> None:
    rmtree("licenses")


def git_init() -> None:
    call("git init")


def process_dependency(dependency: str) -> str:
    """
    >>> process_dependency("pytest")
    'pytest = "*"'
    >>> process_dependency("matplotlib@^3.7.2")
    'matplotlib = "^3.7.2"'
    """
    if not dependency:
        raise ValueError("Blank dependency")

    if len(split := dependency.split("@")) == 1:
        return f'{dependency} = "*"'

    if len(split) != 2:
        raise ValueError(f"Unable to process {dependency=}")

    name, version = split
    return f'{name} = "{version}"'


def process_dependencies(deps: str) -> str:
    """
    >>> process_dependencies(' ')
    ''
    >>> process_dependencies("pytest matplotlib@~3.7 black@!=1.2.3")
    'pytest = "*"\\nmatplotlib = "~3.7"\\nblack = "!=1.2.3"\\n'
    """
    if not deps.strip():
        return ""

    return "\n".join(map(process_dependency, deps.split())) + "\n"


def update_dependencies() -> None:
    # Extra space and .strip() avoids accidentally creating """"
    dependencies = process_dependencies("""{cookiecutter.poetry_dependencies}} """.strip())
    dev_dependencies = process_dependencies("""{{cookiecutter.poetry_dev_dependencies}} """.strip())

    with open("pyproject.toml") as f:
        # Extra space and .strip() prevents issues with quotes
        contents = (
            f.read()
            .replace("{poetry_dependencies}\n", dependencies)
            .replace("{poetry_dev_dependencies}\n", dev_dependencies)
        )
    with open("pyproject.toml", "w") as f:
        f.write(contents)

    call("poetry update")


def install() -> None:
    call("poetry install")


def git_hooks() -> None:
    call("poetry run pre-commit install -t pre-commit", "poetry run pre-commit install -t pre-push")


def git_initial_commit() -> None:
    call("git add .", "git commit -m Setup")


def git_add_remote(name: str, url: str, protocol: PROTOCOL = "git") -> None:
    if protocol == "git":
        _, _, hostname, path = url.split("/", 3)
        url = f"{protocol}@{hostname}:{path}"

    call(f"git remote add {name} {url}")


SUCCESS = "\x1b[1;32m"
TERMINATOR = "\x1b[0m"


def main() -> None:
    set_python_version()
    set_license("{{cookiecutter.license}}")
    remove_license_dir()
    git_init()
    update_dependencies()
    install()
    git_hooks()
    git_initial_commit()
    git_add_remote("origin", "{{cookiecutter.project_url}}")

    print(f"{SUCCESS}Project successfully initialized{TERMINATOR}")


if __name__ == "__main__":
    main()

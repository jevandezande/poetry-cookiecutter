"""Hooks for setting up project once generated."""

import logging
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from typing import Any, Literal

logger = logging.Logger("post_gen_project_logger")
logger.setLevel(logging.INFO)


PROTOCOL = Literal["git", "https"]
GITHUB_PRIVACY_OPTIONS = ["private", "internal", "public"]


def call(*inputs: str, **kwargs: Any) -> None:
    """
    Call shell commands.

    Warning: strings with spaces are not yet supported.
    """
    for input in inputs:
        logger.debug(f"Calling: {input}")
        subprocess.check_call(input.split(), **kwargs)


def set_python_version() -> None:
    """Set the python version in pyproject.toml and .github/workflows/test.yml."""
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
    """
    Copy the licese file to LICENSE (if any).

    :param license: name of the license (or None for no license)
    """
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
    """Remove the licenses directory."""
    rmtree("licenses")


def git_init() -> None:
    """Initialize a git repository."""
    call("git init")


def process_dependency(dependency: str) -> str:
    """
    Process a poetry format dependency.

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
    r"""
    Process a space separated list of poetry format dependencies.

    >>> process_dependencies(' ')
    ''
    >>> process_dependencies("pytest matplotlib@~3.7 black@!=1.2.3")
    'pytest = "*"\nmatplotlib = "~3.7"\nblack = "!=1.2.3"\n'
    """
    if not deps.strip():
        return ""

    return "\n".join(map(process_dependency, deps.split())) + "\n"


def update_dependencies() -> None:
    """Add and update the dependencies in pyproject.toml and poetry.lock."""
    # Extra space and .strip() avoids accidentally creating """"
    dependencies = process_dependencies("""{{cookiecutter.poetry_dependencies}} """.strip())
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
    """Install dependencies."""
    call("poetry install")


def git_hooks() -> None:
    """Install pre-commit and pre-push hooks."""
    call(
        "poetry run pre-commit install -t pre-commit",
        "poetry run pre-commit install -t pre-push",
    )


def git_initial_commit() -> None:
    """Make the initial commit."""
    call("git add .", "git commit -m Setup")


def git_add_remote(name: str, url: str, protocol: PROTOCOL = "git") -> None:
    """
    Add a remote to the git repository.

    :param name: name for the remote
    :param url: url of remote
    :param protocol: protocol of the remote ("git" or "https")
    """
    if protocol == "git":
        _, _, hostname, path = url.split("/", 3)
        url = f"{protocol}@{hostname}:{path}"

    call(f"git remote add {name} {url}")


def github_setup(privacy: str) -> None:
    """
    Make a repository on GitHub (requires GitHub CLI).

    :param privacy: privacy of the repository ("private", "internal", "public")
    """
    if privacy not in GITHUB_PRIVACY_OPTIONS:
        raise ValueError(f"{privacy=} not in {GITHUB_PRIVACY_OPTIONS}")

    try:
        call("gh", stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        raise OSError("The GitHub CLI is not installed; install from https://cli.github.com/")
    except subprocess.CalledProcessError:
        raise OSError("Issue with GitHub CLI encountered")

    call(f"gh repo create {{cookiecutter.package_name}} --{privacy}")


SUCCESS = "\x1b[1;32m"
TERMINATOR = "\x1b[0m"


def main() -> None:
    """Run the post generation hooks."""
    set_python_version()
    set_license("{{cookiecutter.license}}")
    remove_license_dir()
    git_init()
    update_dependencies()
    install()
    git_hooks()
    git_initial_commit()
    git_add_remote("origin", "{{cookiecutter.project_url}}")

    if "{{cookiecutter.github_setup}}" != "None":  # type: ignore
        github_setup("{{cookiecutter.github_setup}}")

    print(f"{SUCCESS}Project successfully initialized{TERMINATOR}")


if __name__ == "__main__":
    main()

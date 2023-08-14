from re import match


def main() -> None:
    check_module_name("{{cookiecutter.package_name}}")


def check_module_name(module_name: str) -> None:
    MODULE_REGEX = r"^[a-zA-Z][_a-zA-Z0-9]+$"

    if not match(MODULE_REGEX, module_name):
        raise ValueError(f"{module_name=} is not a valid Python module name.")


if __name__ == "__main__":
    main()

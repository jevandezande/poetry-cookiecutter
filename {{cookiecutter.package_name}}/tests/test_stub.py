from {{cookiecutter.package_name}}.{{cookiecutter.package_name}} import fib


def test_fib() -> None:
    assert fib(10) == 55

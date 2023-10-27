# Notes

## Adding missing types
Some packages need to have their types added.

```
poetry self add poetry-types
poetry types add <package>
```

## Adding dependencies
Dependencies can be specified in a list, with the @ operator to specify
versions: `dep1@* dep2 dep3@version`. Dependencies that are not tagged to a
specific version (e.g. `dep2`) will have a "\*" appended

## Config file
Make a config file (see [template_config.yml](template_config.yml)) with
default settings and save it as a `.cookiecutterrc` or use it directly via:
`--config-file cookiecutter.yml`

## Running tests with Act
[act](https://github.com/nektos/act) allows one to run GitHub Actions locally
in a docker container. This makes sure all tests are independent of system
settings, and should replicate running these actions on Github.

To run: `act`

## Running scripts
Scripts should be placed in the `[tool.poetry.scripts]` section, and are
formatted as `script_name = path.to.file:function`.

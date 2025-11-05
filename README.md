[![Code Style](https://github.com/equinor/everest-tutorials/actions/workflows/style.yml/badge.svg)](https://github.com/equinor/everest-tutorials/actions/workflows/style.yml)

Everest tutorials



### Style requirements

There are a set of style requirements, which are gathered in the `pre-commit`
configuration, to have it automatically run on each commit do:

```sh
pip install pre-commit
pre-commit install
```

or before each commit do:

```sh
pre-commit run --all-files
```


There is also a pre-push hook configured in `pre-commit` to run a collection of
relatively fast tests, to install this hook:

```sh
pre-commit install --hook-type pre-push
```

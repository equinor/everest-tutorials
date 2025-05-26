# Contributors Guide

Welcome to `everest-tutorials`, the **EVEREST™ Tutorials** repository!
We appreciate your interest in contributing to this project.

We expect all contributors to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).
Be respectful and inclusive in all interactions.

If you have any questions or need assistance, feel free to [open a new issue](https://github.com/equinor/everest-tutorials/issues/new/choose) or [start a new discussion](https://github.com/equinor/everest-tutorials/discussions/new/choose).

Below are the guidelines to help you contribute effectively.

## Introduction

The `everest-tutorials` repository is focused on providing reproducible tutorials for EVEREST.
This is a documentation-based repository with examples and configuration files that focus on practical and reproducible usage.
Contributors are welcome to improve the tutorials, fix bugs, and suggest enhancements to the documentation.

The documentation is built from `main` and is available as a github page in https://equinor.github.io/everest-tutorials/.


## Development Guidelines

### Project organization

The data for each tutorial case is in a directory on the same level as the Drogon ensemble, following the format `/data/drogon/<tutorial_case_name>/`. 
As an example, the well rate optimization experiment is found in `data/drogon/well_rate/`.
As an example, this is the directory layout:

```
data                           # root directory for data
└── drogon                     # Drogon-based tutorials
    ├── fmu-drogon-flow-files  # the git submodule containing the ensemble
    ├── well_rate              # the well rate optimization tutorial
    └── <tutorial_case_name>   # another case using the Drogon ensemble
```

As an examble, within the `well_rate` directory, you find all needed input, templates and configuration files to run the optimization experiment:

```
well_rate
├── everest    # optimization relevant directory
│   ├── input  # input for the optimization case
│   └── model  # optimization model or configuration file
└── simulator  # simulator relevant directory
    └── model  # simulator model or configuration file
```

You can navigate those directories to get examples of the available files. 


### Cloning the repository

The `everest-tutorials` repository includes a git submodule linking to the [`fmu-drogon-flow-files`](https://github.com/equinor/fmu-drogon-flow-files/). This submodule contains the input files needed to run the Drogon examples. If you are interested in working with those files, you will have to clone this repository recursively: 

```bash
git clone --recurse-submodules  https://github.com/equinor/everest-tutorials.git
```

This will clone all files, including the files from the `fmu-drogon-flow-files` repository.

If you are only interested in editing the text files, or work with the other examples, you can clone the repository directly:

```bash
git clone https://github.com/equinor/everest-tutorials.git
```

### Documentation Builds

The documentation is maintained as Python package with all depenencies listed in [pyproject.toml](pyproject.toml). 
The project makes use of `uv` as a package manager, although you can use any other package manager that supports [PEP 518](https://peps.python.org/pep-0518/). 
Once the dependencies are installed, you can use `sphinx-build` to build your documentation:

```bash
sphinx-build -M html ./docs/source ./docs/build/
```

The built documentation is found in the `./docs/build` directory.


### Automatic packaging

All the data added in the `/data/drogon` directory will be packaged and uploaded as release asset to the matching release version.
This is to provide the user with download links containing all the needed files.
The uploaded assets are found in either:

- the latest release: `https://github.com/equinor/everest-tutorials/releases/latest/download/everest-tutorials-drogon.tar.gz`
- a specific release version (e.g v0.4.1): `https://github.com/equinor/everest-tutorials/releases/download/v0.4.1/everest-tutorials-drogon.tar.gz`


### Commit Messages and Pull Requests

#### Commit Messages

This repository follows a specific format for commit messages.
Please ensure that your commit messages are clear and conform to the required style.
We enforce this linting all commit and pull request messages using the [commitlint.yml](https://github.com/equinor/everest-tutorials/blob/main/.github/workflows/commitlint.yml) github action.


#### Commit Message Format

Each commit message consists of a `header`, a `body` and a `footer`. 
The header has a special format that includes a `type`, a `scope` and a `subject`:

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The `header` and the `subject` are mandatory and the rest are optional.
If there is a `body` you need to add a blank line between the header and the body.
If there is `footer` you need to add a blank line between the body and the footer.

The footer can contain a `close` or `fixes` keyword to link to the issue and close it when the pull request is merged. 
This behavior is described in [Linking a pull request to an issue using a keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword).

The accepted types follow the [Angular convention](https://github.com/conventional-changelog/commitlint/tree/master/@commitlint/config-conventional#type-enum) and can be:

| type      | description                                                                                                                |
|-----------|----------------------------------------------------------------------------------------------------------------------------|
| `build`   | Changes that affect the build system or external dependencies (e.g., updating Python, modifying build scripts)             |
| `chore`   | Routine tasks or maintenance changes that do not modify application behavior (e.g., updating dependencies, renaming files) |
| `ci`      | Changes to CI configuration files and scripts (e.g., GitHub Actions)                                                       |
| `docs`    | Documentation-only changes (e.g., updating README, adding comments, refactoring examples)                                  |
| `feat`    | A new feature or functionality added to the codebase                                                                       |
| `fix`     | A bug fix or correction to existing functionality                                                                          |
| `perf`    | Changes that improve performance (e.g., optimizing algorithms, reducing memory usage)                                      |
| `refactor`| Code changes that neither fix a bug nor add a feature but improve code readability or structure                            |
| `revert`  | Reverting a previous commit or change                                                                                      |
| `style`   | Changes that do not affect the meaning of the code (e.g., formatting, whitespace, missing semicolons)                      |
| `test`    | Adding or updating tests (e.g., unit tests, integration tests)                                                             |


As an examples, this is a commit message from the merged pull request #21:

```
feat: added the ensemble as a git submodule
```

And this is a commit message from the automatic release manager:

```
chore(main): release 0.4.1
```


### Pull Request Guidelines

The format of the pull request message is the same as the commit message. 
Ensure your pull request is based on the latest main branch.
Follow the repository's commit message format.
Provide a clear description of the changes in the pull request.
Link any related issues or discussions in the pull request description.
Confirm that all automated checks (such as workflows or actions) pass before requesting a review.



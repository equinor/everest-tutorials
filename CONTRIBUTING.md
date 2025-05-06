# Contributors Guide

Welcome to the **EVEREST™ Tutorials** repository! 
We appreciate your interest in contributing to this project. 

We expect all contributors to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md). 
Be respectful and inclusive in all interactions.

Below are the guidelines to help you contribute effectively.


## Table of Contents

1. [Introduction](#introduction)
2. [Development Guidelines](#development-guidelines)
3. [Commit Messages and Pull Requests](#commit-messages-and-pull-requests)
4. [Packaging and Release Artifacts](#packaging-and-release-artifacts)
5. [Documentation Builds](#documentation-builds)
6. [Getting Help](#getting-help)


## Introduction

The EVEREST Tutorials repository is focused on providing reproducible tutorials for EVEREST. 
This is a documentation-based repository with examples and configuration files that focus on practical usage. 
Contributors are welcome to improve the tutorials, fix bugs, and suggest enhancements to the documentation.


## Development Guidelines

### Drogon model

All provided examples use the Drogon synthetic reservoir model (https://github.com/equinor/fmu-drogon), more specifically the prior of the ensemble output by the iteration `iter-0` (https://github.com/equinor/fmu-drogon-flow-files/).
To avoid duplication, the ensemble data is made available in `/data/drogon/fmu-drogon-flow-files` as a git submodule of the original Drogon repository.


### Tutorial cases

Each tutorial is in a directory on the same level as the Drogon ensemble, following the format `/data/drogon/TUTORIAL_CASE_NAME/`.
As an example, the well rate optimization experiment is found in `data/drogon/well_rate/`.
Within the `well_rate` directory, you find all needed input, templates and configuration files to run the optimization experiment.


### Automatic packaging

All the data added in the `/data/drogon` directory will be packaged and uploaded as release asset to the matching release version.
This is to provide the user with download links containing all the needed files.
The uploaded assets are found in either:

- the latest release: `https://github.com/equinor/everest-tutorials/releases/latest/download/everest-tutorials-drogon.tar.gz`
- a specific release version (e.g v0.4.1): `https://github.com/equinor/everest-tutorials/releases/download/v0.4.1/everest-tutorials-drogon.tar.gz`


### Updating Documentation

Ensure that any changes to the tutorials or examples are reflected in the built documentation.
Documentation files should follow the formatting guidelines below, be concise and easy to read.


## Commit Messages and Pull Requests

### Commit Messages

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


#### Commit Message Examples

From the merged pull request #21:

```
feat: added the ensemble as a git submodule
```

From the automatic release manager:

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


## Getting Help

If you have any questions or need assistance, feel free to [open a new issue](https://github.com/equinor/everest-tutorials/issues/new/choose) or [start a new discussion](https://github.com/equinor/everest-tutorials/discussions/new/choose).

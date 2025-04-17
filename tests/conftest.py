import os
from pathlib import Path
import pytest


@pytest.fixture(scope="session", name="source_root")
def fixture_source_root() -> str:
    current_path = Path(__file__)
    return current_path.parent.parent

def relpath(*path) -> str:
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), *path)

def pytest_addoption(parser):
    parser.addoption("--skip-cleanup", action="store_true", default=False)
    parser.addoption("--release-name", action="store", type=str)
    parser.addoption("--runner-label", action="store", type=str)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="Run tests that require a real MongoDB instance",
    )


def pytest_runtest_setup(item):
    if "live" in item.keywords and not item.config.getoption("--live"):
        pytest.skip("Skipping live MongoDB test (use --live to run)")

import pytest


def pytest_collection_modifyitems(tests):
    """Add timeout mark for slow tests."""
    for test in tests:
        for _ in test.iter_markers(name='slow'):
            test.add_marker(pytest.mark.timeout(2))


@pytest.fixture(autouse=True)
def seed(request):
    """Returns int for fake random seed for registration."""
    return request.config.getoption('randomly_seed')

import pytest


def pytest_collection_modifyitems(items):  # noqa: WPS110
    """Add timeout mark for slow tests."""
    for item in items:  # noqa: WPS110
        for _ in item.iter_markers(name='slow'):
            item.add_marker(pytest.mark.timeout(2))


@pytest.fixture(autouse=True)
def seed(request):
    """Returns int for fake random seed for registration."""
    return request.config.getoption('randomly_seed')

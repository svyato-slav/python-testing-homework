import pytest

from server.apps.identity.container import container
from server.apps.pictures.intrastructure.services import placeholder
from server.apps.pictures.logic.usecases.pictures_fetch import PicturesFetch


def assert_correct_pictures(response, limit) -> None:
    """Assert pictures."""
    assert len(response) == limit
    for picture in response:
        assert isinstance(picture, placeholder.PictureResponse)


@pytest.mark.slow()
@pytest.mark.django_db()
def test_fetch_pictures(
    user,
) -> None:
    """Test fetch pictures work with HTTP."""
    limit = 5
    fetch_pictures = container.instantiate(PicturesFetch)
    response = fetch_pictures(limit=limit)

    assert response
    assert_correct_pictures(response, limit)

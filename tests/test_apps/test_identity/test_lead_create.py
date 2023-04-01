import pytest

from server.apps.identity.container import container
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew


def assert_correct_lead_id(lead_id, user) -> None:
    """Assert lead id."""
    assert user.lead_id == lead_id


@pytest.mark.django_db()
def test_lead_create(
    placeholder_api_url, user,
) -> None:
    """Test leads work with HTTP."""
    user_create_new = container.instantiate(UserCreateNew)
    lead_id = user_create_new(user)
    assert lead_id
    assert_correct_lead_id(lead_id, user)

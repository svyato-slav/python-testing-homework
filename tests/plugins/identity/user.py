import datetime
from typing import Callable, Protocol, TypedDict, final

import pytest
from django_fakery.faker_factory import Factory
from mimesis.schema import Field
from typing_extensions import TypeAlias, Unpack

from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    """
    Represent the simplified user data that is required to create a new user.

    It does not include ``password``, because it is very special in django.
    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime.datetime
    address: str
    job_title: str
    phone: str


@final
class RegistrationData(UserData, total=False):
    """
    Represent the registration data that is required to create a new user.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):  # type: ignore[misc]
    """User data factory protocol."""

    def __call__(
        self,
        **fields: Unpack['RegistrationData'],
    ) -> 'RegistrationData':
        """User data factory protocol."""


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@final
class UserFactory(Protocol):  # type: ignore[misc]
    """A factory to generate a `User` instance."""

    def __call__(self, **fields) -> User:
        """Profile data factory protocol."""


@pytest.fixture()
def mf(seed: int) -> Field:
    """Returns the current mimesis `Field`."""
    return Field(seed=seed)


@pytest.fixture()
def user_password(mf) -> str:
    """Default password for user factory."""
    return mf('person.password')


@pytest.fixture()
def user_email(mf) -> str:
    """Email of the current user."""
    return mf('person.email')


@pytest.fixture()
def user_factory(
    fakery: Factory[User],
    faker_seed: int,
) -> UserFactory:
    """Creates a factory to generate a user instance."""
    def factory(**fields):
        password = fields.pop('password')
        return fakery.make(  # type: ignore[call-overload]
            model=User,
            fields=fields,
            seed=faker_seed,
            pre_save=[lambda _user: _user.set_password(password)],
        )
    return factory


@pytest.fixture()
def user(
    user_factory: UserFactory,
    user_email: str,
    user_password: str,
) -> User:
    """The current user."""
    return user_factory(
        email=user_email,
        password=user_password,
        is_active=True,
    )

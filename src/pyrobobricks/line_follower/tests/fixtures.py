import pytest
from application import Application, State


@pytest.fixture
def application():
    return Application(State())

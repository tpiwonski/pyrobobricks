import pytest
from application import Application


@pytest.fixture
def application():
    return Application()

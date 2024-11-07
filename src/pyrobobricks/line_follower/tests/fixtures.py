from unittest.mock import MagicMock

import pytest
from pyrobobricks.line_follower.application import Application


@pytest.fixture
def application():
    return Application(drive=MagicMock())

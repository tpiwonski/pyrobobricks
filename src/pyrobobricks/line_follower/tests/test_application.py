from unittest.mock import MagicMock
from pyrobobricks.line_follower.application import (
    Application,
    STRAIGHT_FORWARD,
    STRAIGHT_BACKWARD,
    STOP,
    TURN_RIGHT,
    TURN_LEFT,
)
from pyrobobricks.line_follower.path import (
    Position,
    POSITION_LEFT,
    POSITION_OUTSIDE,
    POSITION_RIGHT,
    POSITION_INSIDE,
    POSITION_UNKNOWN,
)


def test_application():
    app = Application(drive=MagicMock())
    app.process(POSITION_LEFT)

    assert app.command == STRAIGHT_FORWARD

    app.process(POSITION_OUTSIDE)

    assert app.command == TURN_RIGHT

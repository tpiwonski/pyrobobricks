

from unittest.mock import MagicMock
from pyrobobricks.line_follower.application import Application, Forward, Backward, Stop, Right, Left
from pyrobobricks.line_follower.path import Position, PositionLeft, PositionOutside, PositionRight, PositionInside, PositionUnknown


def test_application():
    app = Application(drive=MagicMock())
    app.update_move(PositionLeft)

    assert app.move == Forward

    app.update_move(PositionOutside)

    assert app.move == Right

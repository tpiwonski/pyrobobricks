from commands import STRAIGHT_BACKWARD, STRAIGHT_FORWARD, TURN_LEFT, TURN_RIGHT
from path import POSITION_INSIDE, POSITION_LEFT, POSITION_OUTSIDE, POSITION_RIGHT


def test_application_1(application):
    moves = [
        (POSITION_LEFT, STRAIGHT_FORWARD),
        # (POSITION_LEFT, STRAIGHT_FORWARD),
        (POSITION_INSIDE, TURN_LEFT),
        # (POSITION_INSIDE, TURN_LEFT),
        # (POSITION_INSIDE, TURN_LEFT),
        (POSITION_LEFT, STRAIGHT_FORWARD),
    ]

    for position, command in moves:
        application.process(position)
        assert application.command == command, f"{i}: {position}"


def test_application_2(application):
    moves = [
        (POSITION_LEFT, STRAIGHT_FORWARD),
        # (POSITION_LEFT, STRAIGHT_FORWARD),
        (POSITION_INSIDE, TURN_LEFT),
        # (POSITION_INSIDE, TURN_LEFT),
        (POSITION_OUTSIDE, TURN_RIGHT),
        # (POSITION_OUTSIDE, TURN_LEFT),
        (POSITION_LEFT, STRAIGHT_FORWARD),
        # (POSITION_LEFT, STRAIGHT_FORWARD),
    ]

    for i, (position, command) in enumerate(moves):
        application.process(position)
        assert application.command == command, f"{i}: {position}"


def test_application_3(application):
    moves = [
        (POSITION_RIGHT, STRAIGHT_FORWARD),
        # (POSITION_LEFT, STRAIGHT_FORWARD),
        (POSITION_OUTSIDE, TURN_LEFT),
        (POSITION_INSIDE, TURN_RIGHT),
        # (POSITION_OUTSIDE, TURN_LEFT),
        # (POSITION_OUTSIDE, TURN_LEFT),
        (POSITION_RIGHT, STRAIGHT_FORWARD),
        # (POSITION_LEFT, STRAIGHT_FORWARD),
    ]

    for i, (position, command) in enumerate(moves):
        application.process(position)
        assert application.command == command, f"{i}: {position}"


def test_application_4(application):
    moves = [
        (POSITION_INSIDE, STRAIGHT_FORWARD),
        (POSITION_INSIDE, STRAIGHT_FORWARD),
        (POSITION_OUTSIDE, STRAIGHT_BACKWARD),
        (POSITION_INSIDE, STRAIGHT_BACKWARD),
        (POSITION_LEFT, STRAIGHT_FORWARD),
        (POSITION_OUTSIDE, TURN_RIGHT),
    ]

    for i, (position, command) in enumerate(moves):
        application.process(position)
        assert application.command == command, f"{i}: {position}"

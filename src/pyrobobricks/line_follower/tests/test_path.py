from pyrobobricks.line_follower.path import (
    Position,
    Path, SENSOR_POSITION_INSIDE, SENSOR_POSITION_OUTSIDE,
)


def test_foo():
    path = Path()
    assert path.current_index() == -1
    assert path.get_index(0) == -1
    assert path.last_position() is None
    assert path.get_position(0) is None

    position1 = Position.from_sensor_position(
        SENSOR_POSITION_INSIDE, SENSOR_POSITION_INSIDE
    )
    path.add_position(position1)

    assert path.current_index() == 1
    assert path.get_index(0) == 1
    assert path.last_position().left_sensor == position1.left_sensor
    assert path.last_position().right_sensor == position1.right_sensor
    assert path.get_position(0) == path.last_position()

    position2 = Position.from_sensor_position(
        SENSOR_POSITION_OUTSIDE, SENSOR_POSITION_INSIDE
    )
    path.add_position(position2)

    assert path.current_index() == 2
    assert path.get_index(0) == 2
    assert path.get_index(-1) == 1
    assert path.last_position().left_sensor == position2.left_sensor
    assert path.last_position().right_sensor == position2.right_sensor
    assert path.get_position(0) == path.last_position()
    assert path.get_position(-1).left_sensor == position1.left_sensor
    assert path.get_position(-1).right_sensor == position1.right_sensor

    position3 = Position.from_sensor_position(
        SENSOR_POSITION_INSIDE, SENSOR_POSITION_OUTSIDE
    )
    path.add_position(position3)

    assert path.current_index() == 0
    assert path.get_index(0) == 0
    assert path.get_index(-1) == 2
    assert path.get_index(-2) == 1
    assert path.last_position().left_sensor == position3.left_sensor
    assert path.last_position().right_sensor == position3.right_sensor
    assert path.get_position(0) == path.last_position()
    assert path.get_position(-1).left_sensor == position2.left_sensor
    assert path.get_position(-1).right_sensor == position2.right_sensor
    assert path.get_position(-2).left_sensor == position1.left_sensor
    assert path.get_position(-2).right_sensor == position1.right_sensor

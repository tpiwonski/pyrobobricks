from pyrobobricks.line_follower.path import Position, Path, POSITION_INSIDE, POSITION_OUTSIDE

def test_foo():
    path = Path()
    assert path.current_index() == -1
    assert path.get_index(0) == -1
    assert path.last_position() == None
    assert path.get_position(0) == None

    position1 = Position.create(POSITION_INSIDE, POSITION_INSIDE)
    path.add_position(position1)

    assert path.current_index() == 1
    assert path.get_index(0) == 1
    assert path.last_position().left_position == position1.left_position
    assert path.last_position().right_position == position1.right_position
    assert path.get_position(0) == path.last_position()

    position2 = Position.create(POSITION_OUTSIDE, POSITION_INSIDE)
    path.add_position(position2)

    assert path.current_index() == 2
    assert path.get_index(0) == 2
    assert path.get_index(-1) == 1
    assert path.last_position().left_position == position2.left_position
    assert path.last_position().right_position == position2.right_position
    assert path.get_position(0) == path.last_position()
    assert path.get_position(-1).left_position == position1.left_position
    assert path.get_position(-1).right_position == position1.right_position

    position3 = Position.create(POSITION_INSIDE, POSITION_OUTSIDE)
    path.add_position(position3)

    assert path.current_index() == 0
    assert path.get_index(0) == 0
    assert path.get_index(-1) == 2
    assert path.get_index(-2) == 1
    assert path.last_position().left_position == position3.left_position
    assert path.last_position().right_position == position3.right_position
    assert path.get_position(0) == path.last_position()
    assert path.get_position(-1).left_position == position2.left_position
    assert path.get_position(-1).right_position == position2.right_position
    assert path.get_position(-2).left_position == position1.left_position
    assert path.get_position(-2).right_position == position1.right_position


    
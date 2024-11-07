from enum import Enum

from .path import Path


class CommandAction(Enum):
    STOP = 0, 'stop'
    STRAIGHT_FORWARD = 1, 'straight forward'
    STRAIGHT_BACKWARD = 2, 'straight backward'
    TURN_RIGHT = 3, 'turn right'
    TURN_LEFT = 4, 'turn left'


class Command:
    def __init__(self, command=CommandAction.STOP):
        self.command = command

    def __str__(self):
        return f"Command({self.command})"

    def __repr__(self):
        return f"Command({self.command})"


STOP = Command(CommandAction.STOP)
STRAIGHT_FORWARD = Command(CommandAction.STRAIGHT_FORWARD)
STRAIGHT_BACKWARD = Command(CommandAction.STRAIGHT_BACKWARD)
TURN_RIGHT = Command(CommandAction.TURN_RIGHT)
TURN_LEFT = Command(CommandAction.TURN_LEFT)


class Application:
    def __init__(self, drive):
        self.drive = drive
        self.command = STOP
        self.path = Path()

    def process(self, position):
        next_move = STOP

        if self.path.count == 0:
            self.path.add_position(position)
            last_position = position
            # was_outside = position.is_outside()
        else:
            # was_outside = self.path.is_outside
            last_position = self.path.last_position()
            self.path.update_position(position)

        last_side_position = self.path.last_side_position()

        if position.is_inside():
            if self.command == STRAIGHT_BACKWARD:
                if last_position.is_inside():
                    # if last_side_position.is_right():
                    #     next_move = Left
                    # elif last_side_position.is_left():
                    #     next_move = Right
                    # else:
                    next_move = STRAIGHT_BACKWARD  # Forward
                elif last_position.is_right():
                    next_move = TURN_LEFT
                elif last_position.is_left():
                    next_move = TURN_RIGHT
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    if last_side_position.is_right():
                        next_move = TURN_LEFT
                    elif last_side_position.is_left():
                        next_move = TURN_RIGHT
                    else:
                        next_move = STRAIGHT_FORWARD
            else:
                if last_position.is_inside():
                    if last_side_position.is_right():
                        next_move = TURN_RIGHT
                    elif last_side_position.is_left():
                        next_move = TURN_LEFT
                    else:
                        next_move = STRAIGHT_FORWARD
                elif last_position.is_right():
                    next_move = TURN_RIGHT
                elif last_position.is_left():
                    next_move = TURN_LEFT
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    next_move = STRAIGHT_FORWARD

        elif position.is_outside():
            if last_position.is_inside():
                if last_side_position.is_right():
                    next_move = TURN_LEFT
                elif last_side_position.is_left():
                    next_move = TURN_RIGHT
                else:
                    next_move = STRAIGHT_BACKWARD
            elif last_position.is_right():
                next_move = TURN_LEFT
            elif last_position.is_left():
                next_move = TURN_RIGHT
            elif last_position.is_outside() or last_position.unknown():
                next_move = STRAIGHT_FORWARD

        elif position.is_right():
            next_move = STRAIGHT_FORWARD

        elif position.is_left():
            next_move = STRAIGHT_FORWARD

        print(
            f"last side={last_side_position} last position={last_position} position={position} -> {next_move}"
        )

        self.command = next_move

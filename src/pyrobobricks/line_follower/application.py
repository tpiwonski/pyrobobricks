from commands import (
    STOP,
    STRAIGHT_BACKWARD,
    STRAIGHT_FORWARD,
    TURN_LEFT,
    TURN_RIGHT,
    Command,
)
from path import Path, Position


class Application:
    def __init__(self):
        self.command: Command = STOP
        self.path = Path()

    def process(self, position: Position, heading: float = 0):
        next_move = STOP

        if self.path.count == 0:
            self.path.add_position(position)
            last_position = position
        else:
            last_position = self.path.last_position()
            self.path.update_position(position)

        last_side_position = self.path.last_side_position()

        if position.is_inside():
            if self.command.is_command(STRAIGHT_BACKWARD):
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

        print(f"{last_side_position};{last_position};{position};{next_move}")

        if abs(heading) > 140:
            print("XXX")

        self.command = next_move

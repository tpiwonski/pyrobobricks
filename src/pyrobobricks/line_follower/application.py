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

    def process(self, position: Position, heading: float = 0) -> Command:
        command = STOP

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
                        command = TURN_LEFT
                    elif last_side_position.is_left():
                        command = TURN_RIGHT
                    else:
                        command = STRAIGHT_BACKWARD
                elif last_position.is_right():
                    command = TURN_LEFT
                elif last_position.is_left():
                    command = TURN_RIGHT
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    if last_side_position.is_right():
                        command = TURN_LEFT
                    elif last_side_position.is_left():
                        command = TURN_RIGHT
                    else:
                        command = STRAIGHT_FORWARD
            else:
                if last_position.is_inside():
                    if last_side_position.is_right():
                        command = TURN_RIGHT
                    elif last_side_position.is_left():
                        command = TURN_LEFT
                    else:
                        command = STRAIGHT_FORWARD
                elif last_position.is_right():
                    command = TURN_RIGHT
                elif last_position.is_left():
                    command = TURN_LEFT
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    command = STRAIGHT_FORWARD

        elif position.is_outside():
            if last_position.is_inside():
                if last_side_position.is_right():
                    command = TURN_LEFT
                elif last_side_position.is_left():
                    command = TURN_RIGHT
                else:
                    command = STRAIGHT_BACKWARD
            elif last_position.is_right():
                command = TURN_LEFT
            elif last_position.is_left():
                command = TURN_RIGHT
            elif last_position.is_outside() or last_position.unknown():
                command = STRAIGHT_FORWARD

        elif position.is_right():
            command = STRAIGHT_FORWARD

        elif position.is_left():
            command = STRAIGHT_FORWARD

        print(f"{last_side_position};{last_position};{position};{command}")

        if abs(heading) > 140:
            print("XXX")

        self.command = command
        return self.command

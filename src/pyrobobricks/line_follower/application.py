from commands import Command
from path import Path, Position


class State:

    def __init__(self):
        self.path = Path()
        self._command: Command = Command()

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command: Command):
        self._command.action = command.action


class Application:
    def __init__(self, state: State):
        self.state = state

    def process(self, position: Position, heading: float = 0):
        command = Command()

        if self.state.path.count == 0:
            self.state.path.add_position(position)
            last_position = position
        else:
            last_position = self.state.path.last_position()
            self.state.path.update_position(position)

        last_side_position = self.state.path.last_side_position()

        if position.is_inside():
            if self.state.command.is_straight_backward():
                if last_position.is_inside():
                    if last_side_position.is_right():
                        command.turn_left()
                    elif last_side_position.is_left():
                        command.turn_right()
                    else:
                        command.straight_backward()
                elif last_position.is_right():
                    command.turn_left()
                elif last_position.is_left():
                    command.turn_right()
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    if last_side_position.is_right():
                        command.turn_left()
                    elif last_side_position.is_left():
                        command.turn_right()
                    else:
                        command.straight_forward()
            else:
                if last_position.is_inside():
                    if last_side_position.is_right():
                        command.turn_right()
                    elif last_side_position.is_left():
                        command.turn_left()
                    else:
                        command.straight_forward()
                elif last_position.is_right():
                    command.turn_right()
                elif last_position.is_left():
                    command.turn_left()
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    command.straight_forward()

        elif position.is_outside():
            if last_position.is_inside():
                if last_side_position.is_right():
                    command.turn_left()
                elif last_side_position.is_left():
                    command.turn_right()
                else:
                    command.straight_backward()
            elif last_position.is_right():
                command.turn_left()
            elif last_position.is_left():
                command.turn_right()
            elif last_position.is_outside() or last_position.unknown():
                command.straight_forward()

        elif position.is_right():
            command.straight_forward()

        elif position.is_left():
            command.straight_forward()

        print(f"{last_side_position};{last_position};{position};{command}")

        if abs(heading) > 140:
            print("XXX")

        self.state.command = command

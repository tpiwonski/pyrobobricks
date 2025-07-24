from commands import Command
from path import Path, Position


PHASE_MOVE = 1
PHASE_TURN = 2
PHASE_FIND = 3


class State:

    def __init__(self):
        self.path = Path()
        self._command: Command = Command()
        self.phase = PHASE_MOVE

    # @property
    def command(self):
        return self._command

    # @command.setter
    def set_command(self, command: Command):
        self._command.action = command.action


class Application:
    def __init__(self, state: State):
        self.state = state
        self.command = Command()

    def process(self, position: Position, heading: float = 0):
        self.command.stop()

        if self.state.path.count == 0:
            self.state.path.add_position(position)
            last_position = position
        else:
            last_position = self.state.path.last_position()
            self.state.path.update_position(position)

        last_side = self.state.path.last_side_position()

        if self.state.phase in [PHASE_MOVE, PHASE_TURN]:
            self._move(position, heading, last_position, last_side)

        if self.state.phase == PHASE_FIND:
            self._find()
            
        self.state.set_command(self.command)
        return self.state

    def _move(
        self,
        position: Position,
        heading: float,
        last_position: Position,
        last_side: Position,
    ):
        if position.is_inside():
            if self.state.command().is_straight_backward():
                if last_position.is_inside():
                    if last_side.is_right():
                        self.command.turn_left(90)
                    elif last_side.is_left():
                        self.command.turn_right(90)
                    else:
                        self.command.straight_backward(100)
                elif last_position.is_right():
                    self.command.turn_left(90)
                elif last_position.is_left():
                    self.command.turn_right(90)
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    if last_side.is_right():
                        self.command.turn_left(90)
                    elif last_side.is_left():
                        self.command.turn_right(90)
                    else:
                        self.command.straight_forward(100)
            else:
                if last_position.is_inside():
                    if last_side.is_right():
                        self.command.turn_right(90)
                    elif last_side.is_left():
                        self.command.turn_left(90)
                    else:
                        self.command.straight_forward(100)
                elif last_position.is_right():
                    self.command.turn_right(90)
                elif last_position.is_left():
                    self.command.turn_left(90)
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    self.command.straight_forward(100)

        elif position.is_outside():
            if last_position.is_inside():
                if last_side.is_right():
                    self.command.turn_left(90)
                elif last_side.is_left():
                    self.command.turn_right(90)
                else:
                    self.command.straight_backward(100)
            elif last_position.is_right():
                self.command.turn_left(90)
            elif last_position.is_left():
                self.command.turn_right(90)
            elif last_position.is_outside() or last_position.is_unknown():
                self.command.straight_forward(100)

        elif position.is_right():
            self.command.straight_forward(100)

        elif position.is_left():
            self.command.straight_forward(100)

        if abs(heading) > 130:
            # self.state.phase = PHASE_FIND
            pass

    def _find(self):
        pass

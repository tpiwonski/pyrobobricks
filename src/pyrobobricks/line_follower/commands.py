COMMAND_ACTION_STOP = 0
COMMAND_ACTION_STRAIGHT_FORWARD = 1
COMMAND_ACTION_STRAIGHT_BACKWARD = 2
COMMAND_ACTION_TURN_RIGHT = 3
COMMAND_ACTION_TURN_LEFT = 4


class Command:
    def __init__(self, action):
        self.action = action

    def is_command(self, command: "Command") -> bool:
        return self.action == command.action


class Stop(Command):
    def __init__(self):
        super().__init__(COMMAND_ACTION_STOP)

    def __str__(self):
        return "stop"


class StraightForward(Command):
    def __init__(self, distance: int = 0):
        super().__init__(COMMAND_ACTION_STRAIGHT_FORWARD)
        self.distance = distance

    def __str__(self):
        return "straight-forward"


class StraightBackward(Command):
    def __init__(self, distance: int = 0):
        super().__init__(COMMAND_ACTION_STRAIGHT_BACKWARD)
        self.distance = distance

    def __str__(self):
        return "straight-backward"


class TurnLeft(Command):
    def __init__(self, angle: int = 0):
        super().__init__(COMMAND_ACTION_TURN_LEFT)
        self.angle = angle

    def __str__(self):
        return "turn-left"


class TurnRight(Command):
    def __init__(self, angle: int = 0):
        super().__init__(COMMAND_ACTION_TURN_RIGHT)
        self.angle = angle

    def __str__(self):
        return "turn-right"


STOP = Stop()
STRAIGHT_FORWARD = StraightForward()
STRAIGHT_BACKWARD = StraightBackward()
TURN_LEFT = TurnLeft()
TURN_RIGHT = TurnRight()

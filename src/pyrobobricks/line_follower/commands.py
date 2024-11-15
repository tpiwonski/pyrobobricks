STOP = 0
STRAIGHT_FORWARD = 1
STRAIGHT_BACKWARD = 2
TURN_RIGHT = 3
TURN_LEFT = 4


class Command:
    def __init__(self, action=STOP):
        self.action = action

    def stop(self):
        self.action = STOP

    def straight_forward(self):
        self.action = STRAIGHT_FORWARD

    def straight_backward(self):
        self.action = STRAIGHT_BACKWARD

    def turn_right(self):
        self.action = TURN_RIGHT

    def turn_left(self):
        self.action = TURN_LEFT

    def is_stop(self):
        return self.action == STOP

    def is_straight_forward(self):
        return self.action == STRAIGHT_FORWARD

    def is_straight_backward(self):
        return self.action == STRAIGHT_BACKWARD

    def is_turn_right(self):
        return self.action == TURN_RIGHT

    def is_turn_left(self):
        return self.action == TURN_LEFT

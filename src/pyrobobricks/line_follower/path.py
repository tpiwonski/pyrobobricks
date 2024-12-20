SENSOR_POSITION_UNKNOWN = 0
SENSOR_POSITION_OUTSIDE = 1
SENSOR_POSITION_INSIDE = 2


SENSOR_POSITION_TO_STR = {
    SENSOR_POSITION_UNKNOWN: "?",
    SENSOR_POSITION_OUTSIDE: "-",
    SENSOR_POSITION_INSIDE: "+",
}


class Position:
    def __init__(
        self, left_sensor=SENSOR_POSITION_UNKNOWN, right_sensor=SENSOR_POSITION_UNKNOWN
    ):
        self.left_sensor = left_sensor
        self.right_sensor = right_sensor

    def __str__(self):
        return f"Position({SENSOR_POSITION_TO_STR[self.left_sensor]}, {SENSOR_POSITION_TO_STR[self.right_sensor]})"

    def __repr__(self):
        return f"Position({self.left_sensor}, {self.right_sensor})"

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True

        if type(self) != type(other):
            return False

        return (
            self.left_sensor == other.left_sensor
            and self.right_sensor == other.right_sensor
        )

    def __ne__(self, other: object) -> bool:
        return not self == other

    def is_outside(self):
        return (
            self.left_sensor == SENSOR_POSITION_OUTSIDE
            and self.right_sensor == SENSOR_POSITION_OUTSIDE
        )

    def is_inside(self):
        return (
            self.left_sensor == SENSOR_POSITION_INSIDE
            and self.right_sensor == SENSOR_POSITION_INSIDE
        )

    def is_left(self):
        return (
            self.left_sensor == SENSOR_POSITION_OUTSIDE
            and self.right_sensor == SENSOR_POSITION_INSIDE
        )

    def is_right(self):
        return (
            self.left_sensor == SENSOR_POSITION_INSIDE
            and self.right_sensor == SENSOR_POSITION_OUTSIDE
        )

    def is_unknown(self):
        return (
            self.left_sensor == SENSOR_POSITION_UNKNOWN
            or self.right_sensor == SENSOR_POSITION_UNKNOWN
        )

    def copy(self, position):
        self.left_sensor = position.left_sensor
        self.right_sensor = position.right_sensor

    @staticmethod
    def from_sensor_position(left_sensor, right_sensor):
        if (
            left_sensor == SENSOR_POSITION_OUTSIDE
            and right_sensor == SENSOR_POSITION_OUTSIDE
        ):
            return POSITION_OUTSIDE

        if (
            left_sensor == SENSOR_POSITION_INSIDE
            and right_sensor == SENSOR_POSITION_INSIDE
        ):
            return POSITION_INSIDE

        if (
            left_sensor == SENSOR_POSITION_OUTSIDE
            and right_sensor == SENSOR_POSITION_INSIDE
        ):
            return POSITION_LEFT

        if (
            left_sensor == SENSOR_POSITION_INSIDE
            and right_sensor == SENSOR_POSITION_OUTSIDE
        ):
            return POSITION_RIGHT

        if (
            left_sensor == SENSOR_POSITION_UNKNOWN
            or right_sensor == SENSOR_POSITION_UNKNOWN
        ):
            return POSITION_UNKNOWN


POSITION_OUTSIDE = Position(
    left_sensor=SENSOR_POSITION_OUTSIDE, right_sensor=SENSOR_POSITION_OUTSIDE
)
POSITION_INSIDE = Position(
    left_sensor=SENSOR_POSITION_INSIDE, right_sensor=SENSOR_POSITION_INSIDE
)
POSITION_LEFT = Position(
    left_sensor=SENSOR_POSITION_OUTSIDE, right_sensor=SENSOR_POSITION_INSIDE
)
POSITION_RIGHT = Position(
    left_sensor=SENSOR_POSITION_INSIDE, right_sensor=SENSOR_POSITION_OUTSIDE
)
POSITION_UNKNOWN = Position(
    left_sensor=SENSOR_POSITION_UNKNOWN, right_sensor=SENSOR_POSITION_UNKNOWN
)


class Path:

    def __init__(self, positions=None):
        self.positions = positions or [Position(), Position(), Position()]
        self.count = 0
        self.is_outside = False

    def __str__(self):
        return "Path([{}])".format(",".join([p for p in self.positions]))

    def __repr__(self):
        return "Path([{}])".format(",".join([p for p in self.positions]))

    def current_index(self):
        if self.count == 0:
            return -1

        return self.count % len(self.positions)

    def get_index(self, offset):
        if self.count == 0:
            return -1

        return (self.count + offset) % len(self.positions)

    def add_position(self, position):
        self.count += 1
        self.positions[self.current_index()].copy(position)

    def last_position(self):
        if self.count == 0:
            return None

        return self.positions[self.current_index()]

    def get_position(self, offset):
        if self.count == 0:
            return None

        return self.positions[self.get_index(offset)]

    def update_position(self, position: Position):
        if position.is_outside():
            self.is_outside = True
            return

        last_position = self.last_position()

        # if not self.is_outside and last_position.is_left() and position.is_right():
        #     print("SKIP 1")
        #     return

        # if not self.is_outside and last_position.is_right() and position.is_left():
        #     print("SKIP 2")
        #     return

        if position != last_position:
            # print("UPDATE")
            self.add_position(position)

        self.is_outside = False

    def last_side_position(self):
        for offset in [0, -1, -2]:
            position = self.get_position(offset)
            if position.is_left() or position.is_right():
                return position

        return POSITION_UNKNOWN

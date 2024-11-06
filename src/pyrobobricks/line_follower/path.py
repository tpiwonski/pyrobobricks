POSITION_UNKNOWN = 0
POSITION_OUTSIDE = 1
POSITION_INSIDE = 2


def position_to_str(position):
    if position == POSITION_UNKNOWN:
        return '?'
    if position == POSITION_INSIDE:
        return '+'
    if position == POSITION_OUTSIDE:
        return "-"
    
    return ''


class Position:
    def __init__(self, left_position=POSITION_UNKNOWN, right_position=POSITION_UNKNOWN):
        self.left_position = left_position
        self.right_position = right_position

    def __str__(self):
        return f"Position({position_to_str(self.left_position)} {position_to_str(self.right_position)})"

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        
        if type(self) != type(other):
            return False
        
        return self.left_position == other.left_position and self.right_position == other.right_position

    def __ne__(self, other: object) -> bool:
        return not self == other

    def is_outside(self):
        return self.left_position == POSITION_OUTSIDE and self.right_position == POSITION_OUTSIDE

    def is_inside(self):
        return self.left_position == POSITION_INSIDE and self.right_position == POSITION_INSIDE

    def is_left(self):
        return self.left_position == POSITION_OUTSIDE and self.right_position == POSITION_INSIDE

    def is_right(self):
        return self.left_position == POSITION_INSIDE and self.right_position == POSITION_OUTSIDE

    def is_unknown(self):
        return self.left_position == POSITION_UNKNOWN or self.right_position == POSITION_UNKNOWN

    def copy(self, position):
        self.left_position = position.left_position
        self.right_position = position.right_position

    @staticmethod
    def create(left_position, right_position):
        if left_position == POSITION_OUTSIDE and right_position == POSITION_OUTSIDE:
            return PositionOutside
        
        if left_position == POSITION_INSIDE and right_position == POSITION_INSIDE:
            return PositionInside

        if left_position == POSITION_OUTSIDE and right_position == POSITION_INSIDE:
            return PositionLeft
        
        if left_position == POSITION_INSIDE and right_position == POSITION_OUTSIDE:
            return PositionRight
        
        if left_position == POSITION_UNKNOWN or right_position == POSITION_UNKNOWN:
            return PositionUnknown


PositionOutside = Position(POSITION_OUTSIDE, POSITION_OUTSIDE)
PositionInside = Position(POSITION_INSIDE, POSITION_INSIDE)
PositionLeft = Position(POSITION_OUTSIDE, POSITION_INSIDE)
PositionRight = Position(POSITION_INSIDE, POSITION_OUTSIDE)
PositionUnknown = Position(POSITION_UNKNOWN, POSITION_UNKNOWN)


class Path:

    def __init__(self):
        self.positions = [Position(), Position(), Position()]
        self.count = 0
        self.is_outside = False

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
            
        return PositionUnknown
    
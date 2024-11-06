from path import Path


MOVE_STOP = 0
MOVE_FORWARD = 1
MOVE_RIGHT = 2
MOVE_BACKWARD = 3
MOVE_LEFT = 4


class Move:
    def __init__(self, action=MOVE_STOP):
        self.action = action

    def __str__(self):
        if self.action == MOVE_STOP:
            return 'Move(STOP)'
        if self.action == MOVE_FORWARD:
            return 'Move(FORWARD)'
        if self.action == MOVE_RIGHT:
            return 'Move(RIGHT)'
        if self.action == MOVE_BACKWARD:
            return 'Move(BACKWARD)'
        if self.action == MOVE_LEFT:
            return 'Move(LEFT)'
        
        return ''


Stop = Move(MOVE_STOP)
Forward = Move(MOVE_FORWARD)
Backward = Move(MOVE_BACKWARD)
Right = Move(MOVE_RIGHT)
Left = Move(MOVE_LEFT)


class Application:
    def __init__(self, drive):
        self.drive = drive
        self.move = Stop
        self.path = Path()
    
    def update_move(self, position):
        next_move = Stop

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
            if self.move == Backward:
                if last_position.is_inside():
                    # if last_side_position.is_right():
                    #     next_move = Left
                    # elif last_side_position.is_left():
                    #     next_move = Right
                    # else:        
                    next_move = Backward # Forward
                elif last_position.is_right():
                    next_move = Left
                elif last_position.is_left():
                    next_move = Right
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    if last_side_position.is_right():
                        next_move = Left
                    elif last_side_position.is_left():
                        next_move = Right
                    else:
                        next_move = Forward
            else:
                if last_position.is_inside():
                    # if last_side_position.is_right():
                    #     next_move = Right
                    # elif last_side_position.is_left():
                    #     next_move = Left
                    # else:
                    next_move = Forward
                elif last_position.is_right():
                    next_move = Right
                elif last_position.is_left():
                    next_move = Left
                # elif last_position.is_outside() or last_position.is_unknown():
                else:
                    next_move = Forward
        
        elif position.is_outside():
            if last_position.is_inside():
                # if last_side_position.is_right():
                #     next_move = Left
                # elif last_side_position.is_left():
                #     next_move = Right
                # else:        
                next_move = Backward
            elif last_position.is_right():
                next_move = Left
            elif last_position.is_left():
                next_move = Right
            elif last_position.is_outside() or last_position.unknown():
                next_move = Forward
        
        elif position.is_right():
            next_move = Forward

        elif position.is_left():
            next_move = Forward
        
        print(f"last side={last_side_position} last position={last_position} position={position} -> {next_move}")

        self.move = next_move

from pybricks.parameters import Direction, Port, Button
from pybricks.pupdevices import Motor, Remote
from pybricks.robotics import Car
from pybricks.tools import wait

right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
left = Motor(Port.B, Direction.CLOCKWISE)
lift_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
grab_motor = Motor(Port.D, Direction.CLOCKWISE)

remote = Remote()

while True:
    pressed = remote.buttons.pressed()

    rsteering = 1
    lsteering = 1
    if Button.LEFT_PLUS in pressed:
        rsteering = -1
    elif Button.LEFT_MINUS in pressed:
        lsteering = -1

    power = 0
    if Button.LEFT not in pressed:
        if Button.RIGHT_PLUS in pressed:
            power = 100
        elif Button.RIGHT_MINUS in pressed:
            power = -100
    
    right.dc(rsteering * power)
    left.dc(lsteering * power)

    grabbing = 0
    if Button.RIGHT in pressed:
        if Button.LEFT_PLUS in pressed:
            grabbing = 100
        elif Button.LEFT_MINUS in pressed:
            grabbing = -100

    if grabbing == 0:
        grab_motor.stop()
    else:
        grab_motor.run(grabbing)

    lifting = 0
    if Button.LEFT in pressed:
        if Button.RIGHT_PLUS in pressed:
            lifting = 300
        elif Button.RIGHT_MINUS in pressed:
            lifting = -300

    if lifting == 0:
        lift_motor.stop()
    else:
        lift_motor.run(lifting)

    wait(10)
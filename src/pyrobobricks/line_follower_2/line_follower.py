from pybricks.hubs import TechnicHub
from pybricks.parameters import Direction, Port, Color
from pybricks.pupdevices import ColorDistanceSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait

left_sensor = ColorDistanceSensor(Port.C)
right_sensor = ColorDistanceSensor(Port.A)
left_motor = Motor(Port.D, Direction.CLOCKWISE, [12, 40], True)
right_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [12, 40], True)
# drive = DriveBase(left_motor, right_motor, 42, 110)
# drive.settings(40, 200, 60, 300)
hub = TechnicHub()


def calculate_error(reflection):
    if reflection <= 25:
        return 0 # 0 = Black line

    return clamp((reflection - 25) / 25, 0, 1) # Scale to 0-1


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:
    left_reflection = left_sensor.reflection()
    right_reflection = right_sensor.reflection()

    left_error = calculate_error(left_reflection)
    right_error = calculate_error(right_reflection)

    # print("left_reflection=", left_reflection, " left error=", left_error, "right_reflection=", right_reflection, " right error=", right_error)

    # print("left=", left_reflection, " error=", left_error)
    # print("right=", right_reflection, " error=", right_error)

    # left_dc = 30 - (50 * right_error)
    # right_dc = 30 - (50 * left_error)

    # left_dc = map(left_error - right_error, -1, 1, -50, 50)
    # right_dc = map(right_error - left_error, -1, 1, -50, 50)

    # left_dc = 30 + (50 * left_error) - (50 * right_error)
    # right_dc = 30 + (50 * right_error) - (50 * left_error)

    # left_dc = 30 + (left_error - right_error) * 50
    # right_dc = 30 + (right_error - left_error) * 50

    # left_dc = (1 if (left_error - right_error) >= 0 else -1) * map(abs(left_error - right_error), 0, 1, 30, 50)
    # right_dc = (1 if (right_error - left_error) >= 0 else -1) * map(abs(right_error - left_error), 0, 1, 30, 50)

    error = right_error - left_error
    if error < 0:
        left_dc = 30 + 50 * left_error
        right_dc = -50 * left_error
    elif error > 0:
        left_dc = -50 * right_error
        right_dc = 30 + 50 * right_error
    else:
        left_dc = 30
        right_dc = 30

    print("left dc=", left_dc, " right dc=", right_dc)

    left_motor.dc(left_dc)
    right_motor.dc(right_dc)

    wait(10)

"""

1 - 1

im lewy bliżej 1 tym prawy bliżej 0
im prawy bliżej 1 tym lewy bliżej 0

"""

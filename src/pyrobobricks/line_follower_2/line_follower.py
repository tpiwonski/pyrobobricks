from pybricks.hubs import TechnicHub
from pybricks.parameters import Direction, Port, Color
from pybricks.pupdevices import ColorDistanceSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait

left_sensor = ColorDistanceSensor(Port.C)
right_sensor = ColorDistanceSensor(Port.A)
left_motor = Motor(Port.D, Direction.CLOCKWISE, [12, 40], True)
right_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [12, 40], True)
drive = DriveBase(left_motor, right_motor, 42, 110)
drive.settings(40, 200, 60, 300)
hub = TechnicHub()



while True:
    left_reflection = left_sensor.reflection()
    right_reflection = right_sensor.reflection()

    print("left=", left_reflection)
    print("right=", right_reflection)

    wait(500)

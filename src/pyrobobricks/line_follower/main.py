from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task

from path import Position, SENSOR_POSITION_INSIDE, SENSOR_POSITION_UNKNOWN, SENSOR_POSITION_OUTSIDE
from application import (
    Application,
    STRAIGHT_FORWARD,
    STRAIGHT_BACKWARD,
    TURN_LEFT,
    TURN_RIGHT,
    STOP,
)


left_sensor = ColorDistanceSensor(Port.A)
right_sensor = ColorDistanceSensor(Port.B)
left_motor = Motor(Port.C, Direction.CLOCKWISE, [12, 40], True)
right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE, [12, 40], True)
drive = DriveBase(left_motor, right_motor, 42, 110)
# drive.settings(30, 500, 20, 450)
drive.settings(40, 300, 40, 300)

application = Application(drive=drive)


async def read_position():
    left_reflection = await left_sensor.reflection()
    right_reflection = await right_sensor.reflection()

    left_position = (
        SENSOR_POSITION_OUTSIDE if left_reflection > 25 else SENSOR_POSITION_INSIDE
    )
    right_position = (
        SENSOR_POSITION_OUTSIDE if right_reflection > 25 else SENSOR_POSITION_OUTSIDE
    )

    return Position.from_sensor_position(
        left_sensor=left_position, right_sensor=right_position
    )


async def read_position_and_process(app: Application):
    while True:
        position = await read_position()
        app.process(position)
        app.drive.stop()
        await wait(200)


async def execute_command(app):
    while True:
        if app.command == STOP:
            app.drive.brake()
        elif app.command == STRAIGHT_FORWARD:
            await app.drive.straight(100)
        elif app.command == STRAIGHT_BACKWARD:
            await app.drive.straight(-100)
        elif app.command == TURN_LEFT:
            await app.drive.turn(-90)
        elif app.command == TURN_RIGHT:
            await app.drive.turn(90)


async def main(app):
    await multitask(read_position_and_process(app), execute_command(app))


run_task(main(application))

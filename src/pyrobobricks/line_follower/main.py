from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task

from path import POSITION_INSIDE, POSITION_OUTSIDE, Position
from application import Application, Forward, Backward, Left, Right, Stop


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

    left_position = POSITION_OUTSIDE if left_reflection > 25 else POSITION_INSIDE
    right_position = POSITION_OUTSIDE if right_reflection > 25 else POSITION_INSIDE

    return Position.create(left_position=left_position, right_position=right_position)


async def navigate(app: Application):
    while True:
        position = await read_position()
        app.update_move(position)
        app.drive.stop()
        await wait(200)


async def move(app):
    while True:
        if app.move == Stop:
            app.drive.brake()
        elif app.move == Forward:
            await app.drive.straight(100)
        elif app.move == Backward:
            await app.drive.straight(-100)
        elif app.move == Left:
            await app.drive.turn(-90)
        elif app.move == Right:
            await app.drive.turn(90)


async def main(app):
    await multitask(navigate(app), move(app))

run_task(main(application))

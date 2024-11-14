from application import Application
from commands import STOP, STRAIGHT_BACKWARD, STRAIGHT_FORWARD, TURN_LEFT, TURN_RIGHT
from path import SENSOR_POSITION_INSIDE, SENSOR_POSITION_OUTSIDE, Position
from pybricks.hubs import TechnicHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import ColorDistanceSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait

left_sensor = ColorDistanceSensor(Port.A)
right_sensor = ColorDistanceSensor(Port.B)
left_motor = Motor(Port.C, Direction.CLOCKWISE, [12, 40], True)
right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE, [12, 40], True)
drive = DriveBase(left_motor, right_motor, 42, 110)
drive.settings(40, 200, 60, 300)
hub = TechnicHub()

application = Application()


async def read_position() -> Position:
    left_reflection = await left_sensor.reflection()
    right_reflection = await right_sensor.reflection()

    left_position = (
        SENSOR_POSITION_OUTSIDE if left_reflection > 25 else SENSOR_POSITION_INSIDE
    )
    right_position = (
        SENSOR_POSITION_OUTSIDE if right_reflection > 25 else SENSOR_POSITION_INSIDE
    )

    return Position.from_sensor_position(
        left_sensor=left_position, right_sensor=right_position
    )


async def read_position_and_process(app: Application):
    last_command = STOP
    while True:
        position = await read_position()
        heading = hub.imu.heading()
        print(f"heading: {heading}")
        app.process(position, heading)
        if app.command.is_command(TURN_LEFT):
            if not last_command.is_command(TURN_LEFT):
                hub.imu.reset_heading(0)
                print("reset heading")

        elif app.command.is_command(TURN_RIGHT):
            if not last_command.is_command(TURN_RIGHT):
                hub.imu.reset_heading(0)
                print("reset heading")

        last_command = app.command
        drive.stop()
        await wait(200)


async def execute_command(app):
    while True:
        if app.command.is_command(STOP):
            drive.brake()
        elif app.command.is_command(STRAIGHT_FORWARD):
            await drive.straight(100)
        elif app.command.is_command(STRAIGHT_BACKWARD):
            await drive.straight(-100)
        elif app.command.is_command(TURN_LEFT):
            await drive.turn(-90)
        elif app.command.is_command(TURN_RIGHT):
            await drive.turn(90)


async def main(app):
    await multitask(read_position_and_process(app), execute_command(app))


run_task(main(application))

from application import Application, State
from commands import Command
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


class Executor:
    def __init__(self):
        self.command = Command()

    def dispatch_command(self, command: Command):
        if command.is_turn_left() and not self.command.is_turn_left():
            hub.imu.reset_heading(0)

        elif command.is_turn_right() and not self.command.is_turn_right():
            hub.imu.reset_heading(0)

        self.command = command
        drive.stop()


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


async def loop(app: Application, executor: Executor):
    while True:
        position = await read_position()
        heading = hub.imu.heading()
        command = app.process(position, heading)
        executor.dispatch_command(command)
        await wait(200)


async def move(executor: Executor):
    while True:
        if executor.command.is_stop():
            drive.brake()
        elif executor.command.is_straight_forward():
            await drive.straight(100)
        elif executor.command.is_straight_backward():
            await drive.straight(-100)
        elif executor.command.is_turn_left():
            await drive.turn(-90)
        elif executor.command.is_turn_right():
            await drive.turn(90)


async def main(app, executor):
    await multitask(loop(app, executor), move(executor))


state = State()
application = Application(state)
executor = Executor()
run_task(main(application, executor))

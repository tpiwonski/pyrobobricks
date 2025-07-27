from pybricks.hubs import CityHub
from pybricks.parameters import Port, Color
from pybricks.pupdevices import ColorDistanceSensor, DCMotor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait, StopWatch


color_sensor = ColorDistanceSensor(Port.A)
motor = DCMotor(Port.B)
hub = CityHub()

stop_watch = StopWatch()

# RED = Color(h=0, s=94, v=69)
# YELLOW = Color(h=21, s=96, v=93)
# GREEN = Color(h=130, s=97, v=65)
# BLUE = Color(h=220, s=97, v=65)

# WHITE = Color(h=170, s=17, v=99)
# BLACK = Color(h=180, s=65, v=24)

# ORANGE = Color(h=3, s=97, v=86)
# PINK = Color(h=326, s=64, v=98)

# COLORS = [RED, YELLOW, GREEN, BLUE, WHITE, BLACK] 

# COLOR_NAMES = {
#     RED: 'RED',
#     YELLOW: 'YELLOW',
#     GREEN: 'GREEN',
#     BLUE: 'BLUE',
#     WHITE: 'WHITE',
#     BLACK: 'BLACK',
# }

# Color.RED = Color(h=0, s=90, v=60)
# Color.YELLOW = Color(h=30, s=100, v=100)
# Color.WHITE = Color(h=100, s=10, v=100)

# color_sensor.detectable_colors([Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.WHITE, Color.NONE])

STOP = 0
MOVE = 1

command = STOP

async def loop():
    global command
    while True:
        # position = await read_position()
        # heading = hub.imu.heading()
        # app.process(position, heading)
        # executor.dispatch_command(app.state.command())

        # color = await color_sensor.hsv()
        # print(color)
        color = await color_sensor.color()
        # color_name = COLOR_NAMES.get(color)
        print(color, color.h, color.s, color.v)
                
        if color == Color.RED:
            if command == MOVE and stop_watch.time() < 1000:
                pass
            
            else:
                if command != STOP:
                    stop_watch.reset()

                command = STOP            
        else:
            command = MOVE

        if command == STOP and stop_watch.time() > 3000:
            stop_watch.reset()
            command = MOVE

        await wait(50)


async def move():
    while True:
        if command == MOVE:
            motor.dc(75)
        elif command == STOP:
            motor.brake()

        # if executor.command.is_stop():
        #     drive.brake()
        #     hub.light.on(Color.RED)
        # elif executor.command.is_straight_forward():
        #     await drive.straight(100)
        #     hub.light.on(Color.GREEN)
        # elif executor.command.is_straight_backward():
        #     await drive.straight(-100)
        #     hub.light.on(Color.YELLOW)
        # elif executor.command.is_turn_left():
        #     await drive.turn(-90)
        #     hub.light.on(Color.ORANGE)
        # elif executor.command.is_turn_right():
        #     await drive.turn(90)
        #     hub.light.on(Color.BLUE)
        await wait(50)
        # print('MOVING')


async def main():
    await multitask(loop(), move())


run_task(main())

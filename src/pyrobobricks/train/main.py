from pybricks.hubs import CityHub
from pybricks.parameters import Port, Color, Button
from pybricks.pupdevices import ColorDistanceSensor, DCMotor, Remote
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch

sensor = ColorDistanceSensor(Port.A)
motor = DCMotor(Port.B)
hub = CityHub()
remote = Remote()

MODE_MANUAL = 0
MODE_AUTO = 1

SPEED_FAST = 80
SPEED_NORMAL = 60
SPEED_SLOW = 40

STOP_TIME = 3000

class State:
    def enter(self):
        pass

    def process(self, color: Color):
        pass

    def exit(self):
        pass

class StoppedState(State):
    watch: StopWatch

    def __init__(self):
        self.watch = StopWatch()

    def enter(self):
        self.watch.reset()        
        set_command(Stop)

    def process(self, color):
        if self.watch.time() >= STOP_TIME:
            set_state(MovingForward)


class MovingForwardState(State):
    watch: StopWatch

    def __init__(self):
        self.watch = StopWatch()

    def enter(self):
        self.watch.reset()
        MoveForward.set_dc(SPEED_NORMAL)
        set_command(MoveForward)

    def process(self, color):
        if color == Color.RED and self.watch.time() >= 300:
            set_state(Stopped)
        elif color == Color.YELLOW:
            MoveForward.set_dc(SPEED_SLOW)
        elif color == Color.BLUE:
            MoveForward.set_dc(SPEED_FAST)
        elif color == Color.GREEN:
            MoveForward.set_dc(SPEED_NORMAL)


class Command:
    def process(self):
        pass


class StopCommand(Command):
    def process(self):
        motor.brake()
        motor.dc(0)


class MoveForwardCommand(Command):
    dc = 0

    def set_dc(self, dc):
        if dc >= -100 and dc <= 100:
            self.dc = dc

    def chg_dc(self, dc):
        self.set_dc(self.dc + dc)

    def process(self):
        motor.dc(self.dc)


Stopped = StoppedState()
MovingForward = MovingForwardState()

Stop = StopCommand()
MoveForward = MoveForwardCommand()

app_state = Stopped
app_command = Stop

mode = MODE_MANUAL

watch = StopWatch()
colors = [Color.NONE, Color.NONE, Color.NONE, Color.NONE, Color.NONE]

ColorUnknown = Color(h=200, s=50, v=30)
Color.GREEN = Color(h=130, s=90, v=50)

sensor.detectable_colors([Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.WHITE, Color.NONE, ColorUnknown])

def set_state(state: State):
    global app_state

    app_state.exit()
    app_state = state
    app_state.enter()


def set_command(command: Command):
    global app_command

    app_command = command

pressing = set()

while True:
    pressed = remote.buttons.pressed()
    # print(pressed)

    if Button.LEFT in pressed and Button.LEFT not in pressing:
        if mode == MODE_MANUAL:
            mode = MODE_AUTO
            set_state(MovingForward)
            remote.light.on(Color.WHITE)
        else:
            mode = MODE_MANUAL
            # MoveForward.set_dc(0)
            set_command(MoveForward)
            hub.light.on(Color.BLUE)
            remote.light.on(Color.BLUE)

    elif Button.RIGHT in pressed and Button.RIGHT not in pressing:
            mode = MODE_MANUAL
            MoveForward.set_dc(0)
            set_command(MoveForward)
            MoveForward.process()
            hub.light.on(Color.BLUE)
            remote.light.on(Color.BLUE)

    if mode == MODE_AUTO:
        color = sensor.color()
        if color in [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.WHITE]:
            hub.light.on(color)            
        else:
            hub.light.on(Color.WHITE)            
        
        app_state.process(color)
        app_command.process()
    else:
        if Button.RIGHT_PLUS in pressed and Button.RIGHT_PLUS not in pressing:
            MoveForward.chg_dc(10)
            MoveForward.process()
            # watch.reset()
        elif Button.RIGHT_MINUS in pressed and Button.RIGHT_MINUS not in pressing:
            MoveForward.chg_dc(-10)
            MoveForward.process()
            # watch.reset()
        # elif Button.RIGHT in pressed:
        #     MoveForward.set_dc(0)
        #     MoveForward.process()

    pressing = pressed.copy()

from rf300pwm import *

INPUT = False
OUTPUT = True
HIGH = True
LOW = False
NV_UNIT = 128
NV_GROUP = 129
NV_GROUP_SIZE = 130
NV_GROUP_INTEREST_MASK_ID = 5
NV_GROUP_FORWARDING_MASK_ID = 6

PIN_RED = 0
PIN_GREEN = 1
PIN_BLUE = 2
PIN_NOTHING = 3

my_group = None
my_group_size = 32
my_unit = None
sleep_mode = False
current_effect = 0

state_last_ms = 0
state_counter_max = 5000
state_my_turn = False
state_rainbow = 0

set_r = 102
set_g = 47
set_b = 142
current_r = 0
current_g = 32
current_b = 0
last_written_r = -1
last_written_g = -1
last_written_b = -1

def max(a, b):
    if a > b:
        return a
    return b

@setHook(HOOK_STARTUP)
def init():
    setPinDir(PIN_RED, OUTPUT)
    setPinDir(PIN_GREEN, OUTPUT)
    setPinDir(PIN_BLUE, OUTPUT)
    writePin(PIN_RED, LOW)
    writePin(PIN_GREEN, LOW)
    writePin(PIN_BLUE, LOW)

    initTimer0_8bit()
    Init_PWM_GPIO(PIN_RED)
    Init_PWM_GPIO(PIN_GREEN)
    Init_PWM_GPIO(PIN_BLUE)

    write_color(100, 0, 0) #while we boot.

    set_group(loadNvParam(NV_GROUP), loadNvParam(NV_GROUP_SIZE))
    set_unit(loadNvParam(NV_UNIT))

    write_color(0, 0, 0)

@setHook(HOOK_100MS)
def main_loop():
    if not sleep_mode:
        run_effect(current_effect)


@setHook(HOOK_1S)
def hook_1s():
    provisioning = False

    if my_group is None:
        provisioning = True
        set_color(32, 0, 0)
    elif my_unit is None:
        provisioning = True
        set_color(0, 0, 32)
    
    if provisioning:
        if current_effect != 2:
            set_current_effect(0) #pilot
        set_counter_max(2000)
    else:
        if current_effect == 2:
            set_current_effect(0)

    
    if sleep_mode:
        sleep(0, 15) #seconds


def set_group(x, size=32):
    global my_group, my_group_size
    my_group = x
    my_group_size = size
    saveNvParam(NV_GROUP, x)
    saveNvParam(NV_GROUP_SIZE, size)

    x = x | 1 #ALWAYS subscribe to the broadcast group
    saveNvParam(NV_GROUP_INTEREST_MASK_ID, x)
    saveNvParam(NV_GROUP_FORWARDING_MASK_ID, x)
def get_group():
    return my_group

def set_unit(y):
    global my_unit
    my_unit = y
    saveNvParam(NV_UNIT, y)
def get_unit():
    return my_unit

def set_group_and_unit(x, y):
    set_group(x)
    set_unit(y)

def set_sleep_mode(b):
    global sleep_mode
    sleep_mode = b
    write_color(0, 0, 0)


def write_color(r, g, b):
    global last_written_r, last_written_g, last_written_b

    if r != last_written_r:
        if r == 0 or last_written_r == 0:
            set_push_pull(PIN_RED, r>0)
        SetDutyCycle(PIN_RED, 255-r)
        last_written_r = r

    if g != last_written_g:
        if g == 0 or last_written_g == 0:
            set_push_pull(PIN_GREEN, g>0)
        SetDutyCycle(PIN_GREEN, 255-g)
        last_written_g = g

    if b != last_written_b:
        if b == 0 or last_written_b == 0:
            set_push_pull(PIN_BLUE, b>0)
        SetDutyCycle(PIN_BLUE, 255-b)
        last_written_b = b

def set_current_effect(e):
    global current_effect
    current_effect = e


def set_last_ms(offset=0):
    global state_last_ms
    state_last_ms = getMs() + offset
def shuffle():
    set_last_ms(getMs() - random())
    pulsePin(PIN_NOTHING, random())
    set_color(random() % 255, random() % 255, random() % 255)
def set_counter_max(x):
    global state_counter_max
    state_counter_max = x
def trip_color():
    global current_r, current_g, current_b
    current_r, current_g, current_b = set_r, set_g, set_b
def set_color(r, g, b):
    global set_r, set_g, set_b, current_r, current_g, current_b

    set_r, set_g, set_b = r%255, g%255, b%255
    trip_color()
def reset_rainbow(offset=50):
    global state_rainbow
    state_rainbow = 0 + ( my_unit * offset )
def next_color_in_rainbow():
    global state_rainbow, current_r, current_g, current_b
    
    if state_rainbow >= 1536:
        state_rainbow = 0
    else:
        state_rainbow += 10

    if state_rainbow < 256:
        current_b = 255 - (state_rainbow % 256)
        current_r = 255
    elif state_rainbow < 512:
        current_r = 255
        current_g = state_rainbow % 256
    elif state_rainbow < 768:
        current_r = 255 - (state_rainbow % 256)
        current_g = 255
    elif state_rainbow < 1024:
        current_g = 255
        current_b = state_rainbow % 256
    elif state_rainbow < 1280:
        current_g = 255 - (state_rainbow % 256)
        current_b = 255
    elif state_rainbow < 1536:
        current_b = 255
        current_r = state_rainbow % 256


def set_my_turn(unit):
    global state_my_turn
    if my_unit == unit:
        state_my_turn = True

def run_effect(effect):
    global current_r, current_g, current_b, state_last_ms, state_my_turn
    if effect == 0:
        """Pilot light"""
        if getMs() - state_last_ms > state_counter_max:
            write_color(current_r, current_g, current_b)
            set_last_ms()
        else:
            write_color(0, 0, 0)
    elif effect == 1:
        """BlinkSync"""
        if getMs() - state_last_ms > state_counter_max + 25:
            mcastRpc(my_group, 1, "set_last_ms")
        run_effect(0)
    elif effect == 2:
        """ID"""
        if ( getMs() / 10 ) % 2 == 0:
            write_color(128, 128, 128)
        else:
            write_color(0, 0, 0)
    elif effect == 10:
        """Confettoply"""
        run_effect(11)
        if current_r <= 0: current_r = 200
        if current_g <= 0: current_g = 200
        if current_b <= 0: current_b = 200

    elif effect == 11:
        """Fade Out"""
        current_r -= 10
        current_g -= 10
        current_b -= 10
        if current_r < 0: current_r = 0
        if current_g < 0: current_g = 0
        if current_b < 0: current_b = 0
        write_color(current_r, current_g, current_b)

    elif effect == 12:
        """Chase"""
        run_effect(11)
        
        if state_my_turn:
            trip_color()
            state_my_turn = False

            friend = my_unit+1
            if friend > my_group_size:
                friend = 1
            
            mcastRpc(my_group, 1, "set_my_turn", friend)
            set_last_ms()
        
        if getMs() - state_last_ms > state_counter_max:
            state_my_turn = True
            set_last_ms()

    elif effect == 13:
        """Rainbow"""
        next_color_in_rainbow()
        write_color(current_r, current_g, current_b)


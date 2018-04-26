from rf300pwm import *

INPUT = False
OUTPUT = True
HIGH = True
LOW = False
NV_UNIT = 128
NV_GROUP = 129
NV_GROUP_INTEREST_MASK_ID = 5
NV_GROUP_FORWARDING_MASK_ID = 6

PIN_RED = 0
PIN_GREEN = 1
PIN_BLUE = 2

my_group = None
my_unit = None
sleep_mode = False
current_effect = 0

state_last_ms = 0
state_counter_max = 5000

current_r = 102
current_g = 47
current_b = 142
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

    write_color(255, 0, 0) #while we boot.

    set_group(loadNvParam(NV_GROUP))
    set_unit(loadNvParam(NV_UNIT))

    write_color(0, 0, 0)

@setHook(HOOK_100MS)
def main_loop():
    if not sleep_mode:
        run_effect(current_effect)


@setHook(HOOK_1S)
def hook_1s():
    if my_group is None:
        pulsePin(PIN_BLUE, 25, True)
    elif my_unit is None:
        pulsePin(PIN_RED, 25, True)
    
    if sleep_mode:
        sleep(0, 15) #seconds


def set_group(x):
    global my_group
    my_group = x
    saveNvParam(NV_GROUP, x)

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
def set_counter_max(x):
    global state_counter_max
    state_counter_max = x

def run_effect(effect):
    global current_r, current_g, current_b, state_last_ms
    if effect == 0:
        """Pilot light"""
        if getMs() - state_last_ms > state_counter_max:
            write_color(current_r, current_g, current_b)
            set_last_ms()
        else:
            write_color(0, 0, 0)
    elif effect == 1:
        """BlinkSync"""
        if getMs() - state_last_ms > state_counter_max:
            mcastRpc(my_group, 1, "set_last_ms", -25)
        run_effect(0)
    elif effect == 2:
        """Confettoply"""
        current_r += 10
        current_g += 10
        current_b += 10
        if current_r > 255: current_r = 0
        if current_g > 255: current_g = 0
        if current_b > 255: current_b = 0

        write_color(current_r, current_g, current_b)


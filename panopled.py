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
counter = 1000 #skip first blink
counter_max = 10000
current_effect = 0

current_r = 102
current_g = 47
current_b = 142
last_r = 0
last_g = 0
last_b = 0

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

@setHook(HOOK_10MS)
def hook_10ms():
    global counter

    if not sleep_mode:
        run_effect(current_effect)

    if counter >= counter_max:
        counter = 0
    else:
        counter += 10

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
    SetDutyCycle(PIN_RED, 255-r)
    SetDutyCycle(PIN_GREEN, 255-g)
    SetDutyCycle(PIN_BLUE, 255-b)

def set_current_effect(e):
    global current_effect
    current_effect = e

def set_counter(n):
    global counter
    counter = n

def set_counter_max(n):
    global counter_max
    counter_max = n

def run_effect(effect):
    if effect == 0:
        """Blink"""
        if counter <= 25:
            write_color(0, 32, 0) #pulsePin(PIN_GREEN, 25, True)
        else:
            write_color(0, 0, 0)
    elif effect == 1:
        """BlinkSync"""
        if counter >= counter_max:
            mcastRpc(my_group, 1, "set_counter", 0)
        run_effect(0) #Blink
    elif effect == 2:
        """Drip"""
        if counter < 100:
            write_color(current_r, current_g, current_b)
        else:
            write_color(current_r / (counter*100), current_g / (counter*100), current_b / (counter*100))


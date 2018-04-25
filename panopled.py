INPUT = False
OUTPUT = True
HIGH = True
LOW = False
NV_UNIT = 128
NV_GROUP = 129
NV_GROUP_INTEREST_MASK_ID = 5
NV_GROUP_FORWARDING_MASK_ID = 6

PIN_RED = 10
PIN_GREEN = 11
PIN_BLUE = 12

my_group = None
my_unit = None
sleep_mode = False
counter = 0
counter_max = 10000
current_effect = 0

@setHook(HOOK_STARTUP)
def init():
    setPinDir(PIN_RED, OUTPUT)
    writePin(PIN_RED, LOW)
    setPinDir(PIN_GREEN, OUTPUT)
    writePin(PIN_GREEN, LOW)
    setPinDir(PIN_BLUE, OUTPUT)
    writePin(PIN_BLUE, LOW)

    set_color(255, 0, 0) #while we boot.

    set_group(loadNvParam(NV_GROUP))
    set_unit(loadNvParam(NV_UNIT))

    set_color(0, 0, 0)

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
    set_color(0, 0, 0)


def set_color(r, g, b):
    #Stub version that only supports on/off
    writePin(PIN_RED, r > 0)
    writePin(PIN_GREEN, g > 0)
    writePin(PIN_BLUE, b > 0)

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
        if counter == 0:
            pulsePin(PIN_GREEN, 25, True)
    elif effect == 1:
        """BlinkSync"""
        if counter >= counter_max:
            mcastRpc(my_group, 1, "set_counter", 0)
        if counter <= 25:
            pulsePin(PIN_GREEN, 25, True) 

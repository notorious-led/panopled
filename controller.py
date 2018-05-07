target = -1
count = 0

@setHook(HOOK_STARTUP)
def boot():
    pin = 0
    while pin <= 10:
        monitorPin(pin, True)
        setPinPullup(pin, True)
        pin += 1

@setHook(HOOK_1S)
def one_second():
    if count < 60:
        if target == 0:
            mcastRpc(1, 1, "set_sleep_mode", True)
        else:
            mcastRpc(1, 1, "set_sleep_mode", False)
            
    if count < 5:
        mcastRpc(1, 1, "set_current_effect", target)
        if target == 120:
            mcastRpc(1, 1, "write_color_for_unit", 1, 0xef, 0x51, 0x38)
            mcastRpc(1, 1, "write_color_for_unit", 2, 0xf1, 0xbf, 0x4e)
            mcastRpc(1, 1, "write_color_for_unit", 3, 0x58, 0xb4, 0x9b)
            mcastRpc(1, 1, "write_color_for_unit", 4, 0x10, 0xa0, 0xc2)
            mcastRpc(1, 1, "write_color_for_unit", 5, 0x80, 0x80, 0x80)
            mcastRpc(1, 1, "write_color_for_unit", 6, 0x80, 0x80, 0x80)
            mcastRpc(1, 1, "write_color_for_unit", 7, 0x80, 0x80, 0x80)
            mcastRpc(1, 1, "write_color_for_unit", 8, 0x80, 0x80, 0x80)



@setHook(HOOK_GPIN)
def thing(pin, is_it):
    global target

    print(pin)

    if pin == 4: #2
        target = 10 #confettoply
    elif pin == 0: #5
        target = 120 #static color
    elif pin == 1: #6
        target = 13 #rainbow
    else: #* (pin 10)
        target = 0

    count = 0





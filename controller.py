target = 1
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
    global count

    if count < 60:
        count += 1

        if target == 0:
            mcastRpc(1, 1, "set_sleep_mode", True)
        else:
            mcastRpc(1, 1, "set_sleep_mode", False)
            
    if count < 30:
        mcastRpc(1, 1, "set_current_effect", target)
        if target == 120:
            if count % 10 == 1:
                mcastRpc(1, 1, "write_color_for_unit", 1, 64, 0, 0)
            if count % 10 == 2:
                mcastRpc(1, 1, "write_color_for_unit", 2, 64, 64, 0)
            if count % 10 == 3:
                mcastRpc(1, 1, "write_color_for_unit", 3, 0, 64, 0)
            if count % 10 == 4:
                mcastRpc(1, 1, "write_color_for_unit", 4, 0, 0, 64)
            if count % 10 == 5:
                mcastRpc(1, 1, "write_color_for_unit", 5, 48, 48, 48)
            if count % 10 == 6:
                mcastRpc(1, 1, "write_color_for_unit", 6, 48, 48, 48)
            if count % 10 == 7:
                mcastRpc(1, 1, "write_color_for_unit", 7, 48, 48, 48)
            if count % 10 == 8:
                mcastRpc(1, 1, "write_color_for_unit", 8, 48, 48, 48)

        



@setHook(HOOK_GPIN)
def thing(pin, is_it):
    global target, count

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





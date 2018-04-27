target = -1

@setHook(HOOK_STARTUP)
def boot():
    pin = 0
    while pin <= 10:
        monitorPin(pin, True)
        setPinPullup(pin, True)
        pin += 1

@setHook(HOOK_GPIN)
def thing(pin, is_it):
    global target

    print(pin)

    if pin == 4: #2
        target = 10 #confettoply
    elif pin == 0: #5
        target = 12 #chase
    elif pin == 1: #6
        target = 13 #rainbow
    else: #* (pin 10)
        target = 0

    if target == 0:
        mcastRpc(1, 1, "set_color", random()%255, random()%255, random()%255)

    if not is_it:
        mcastRpc(1, 1, "set_current_effect", target)
    if is_it and target == 13:
        mcastRpc(1, 1, "reset_rainbow")




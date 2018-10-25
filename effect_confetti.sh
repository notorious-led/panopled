#!/usr/bin/env bash

echo -n "Changing effect once "
snap rpc send multicast set_current_effect 10

for I in $(seq 0 4); do
    echo -n "$I Changing color "

    #snap rpc send multicast set_color 0xef 0x51 0x38
    snap rpc send multicast set_color 0xcf 0x51 0x08
    snap rpc send multicast set_current_effect 10

    sleep 0.1
done


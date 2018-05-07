#!/usr/bin/env bash

for I in $(seq 0 4); do
    echo -n "$I Changing color and effect "

    snap rpc send multicast set_color 0xef 0x51 0x38
    snap rpc send multicast set_current_effect 10

    sleep 0.1
done


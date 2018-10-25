#!/usr/bin/env bash

for I in $(seq 0 2); do
    echo -n "$I Changing effect and setting colors "

    snap rpc send multicast set_color 200 0 200
    snap rpc send multicast set_current_effect 12

    sleep 0.1
done


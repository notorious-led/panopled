#!/usr/bin/env bash

for I in $(seq 0 2); do
    echo -n "$I Fading to black "

    snap rpc send multicast set_current_effect 11

    sleep 0.1
done


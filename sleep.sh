#!/usr/bin/env bash

for I in $(seq 0 60); do
    echo -n "$I "
    snap rpc send multicast set_sleep_mode True
    sleep 0.1
done


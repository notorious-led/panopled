#!/usr/bin/env bash

for I in $(seq 0 60); do
    echo -n "$I "
    snap rpc send multicast set_sleep_mode False
    sleep 0.1
done

for I in $(seq 0 2); do
    echo -n "$I REBOOT "
    snap rpc send multicast reboot
    sleep 0.1
done



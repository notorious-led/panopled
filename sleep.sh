#!/usr/bin/env bash

for I in $(seq 0 4); do
    echo -n "$I Setting effect "
    snap rpc send multicast set_current_effect 11
    sleep 0.1
done
for I in $(seq 0 4); do
    echo -n "$I Sending sleep command "
    snap rpc send multicast set_sleep_mode True
    sleep 0.1
done


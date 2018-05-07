#!/usr/bin/env bash

for I in $(seq 0 4); do
    echo -n "$I Changing effect "

    snap rpc send multicast set_current_effect 13

    sleep 0.1
done


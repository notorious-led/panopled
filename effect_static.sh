#!/usr/bin/env bash

for I in $(seq 0 2); do
    echo -n "$I Changing effect and setting colors "

    snap rpc send multicast set_current_effect 121
    #snap rpc send multicast write_color_for_unit 1 64 0 0
    #snap rpc send multicast write_color_for_unit 2 64 64 0 0
    #snap rpc send multicast write_color_for_unit 3 0 64 0
    #snap rpc send multicast write_color_for_unit 4 0 0 64
    #snap rpc send multicast write_color_for_unit 5 48 48 48
    #snap rpc send multicast write_color_for_unit 6 48 48 48 
    #snap rpc send multicast write_color_for_unit 7 48 48 48
    #snap rpc send multicast write_color_for_unit 8 48 48 48

    sleep 0.1
done


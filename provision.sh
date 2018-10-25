#!/usr/bin/env bash

set -e

echo -n "Bridge: "
BRIDGE="$(snap node bridge info | grep address | cut -d ':' -f 6-8 | sed 's/://g')"
echo "$BRIDGE"

echo -n "TEMP: Setting all nodes to group 1, "
snap rpc send multicast set_group 1
snap rpc send multicast set_group 1 2>&1 > /dev/null

echo "Finding nodes"
NODES="$(snap rpc call multicast ffffff get_group 2>&1 | pv -l | grep --line-buffered "Received unexpected mcast" | awk '{print $NF}' | sort -u | xargs )"

for NODE in $NODES; do
    echo -n "$NODE: "
    if [ "$NODE" == "$BRIDGE" ]; then
        echo "bridge node."
        continue
    fi

    CURRENT="$(snap rpc call unicast $NODE get_unit 2>/dev/null | cut -d '(' -f 2 | cut -d ',' -f 1)"
    echo -n "$CURRENT "
    if [ "$CURRENT" != "None" ]; then
        echo "already set."
        continue
    fi
    
    ( snap rpc send unicast $NODE set_current_effect 2 >/dev/null 2>/dev/null; snap rpc send unicast $NODE set_current_effect 2 >/dev/null 2>/dev/null ) &
    read -p "new: " NEW_ID
    if [ "$NEW_ID" != "" ]; then
        snap rpc call unicast $NODE set_unit $NEW_ID 2>/dev/null >/dev/null
        snap rpc call unicast $NODE set_color 0 1 0 2>/dev/null >/dev/null
    fi
done

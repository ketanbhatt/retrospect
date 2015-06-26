#!/bin/bash

for i in `seq 1 10`;
        do
                xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) _NET_WM_NAME WM_CLASS | cut -d" " -f3- >> output.txt
                sleep 1
        done
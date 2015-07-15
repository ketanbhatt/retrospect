#!/bin/bash

sudo pip install python-xlib-0.15rc1.tar.gz
sudo apt-get install redis-server
sudo pip install redis

nohup redis-server &

exit
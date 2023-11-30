#!/bin/bash

# start JS proxy-server
node proxy.js&

# start Python server
cd ../code;
python3 ./server.py &


# sleep
sleep infinity

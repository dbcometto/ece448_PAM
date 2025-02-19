# This is the python script that will decode the FSK ascii data using push/pull
# Written by Ben Cometto, 18 Feb 2025

import zmq
import struct
import sys
import time


current_time = 0
last_time = 0
period_ms = 100

# variables
socket_loc = "tcp://localhost:4444"


#  Set up socket to talk to GNU Radio
context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
pull_socket.setsockopt(zmq.CONFLATE, 1)
pull_socket.connect(socket_loc)

print(f" I am setup and waiting for messages on {socket_loc}")


# Main Processing Loop
while True: 

    current_time = time.time()*1000

    if (current_time-last_time) > 100:
        # Get new data
        try:
            print(pull_socket.recv(flags=zmq.NOBLOCK).decode("cp1252"))
        except:
            pass   

        last_time = current_time
        
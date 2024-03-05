import tornado.ioloop
import random
import re
#import tornado.web
import tornado.websocket
import socket
import os
#import tornado.gen
import threading, time
from threading import Timer 

# SERVER IP
# Get the external IP address
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("0.0.0.0", 80))  
#IPAddress = s.getsockname()[0]
#IPAddress = "10.0.2.2" # STANDARD FOR ANDROID STUDIO
IPAddress = "0.0.0.0" # CONNECT TO ALL PORTS
print('Your Computer IP Address is: ' + IPAddress)

# Set the Server IP as the local host (of my PC)
server_port = "8888"
#print("Websocket server for Pepper listening on port: " +  server_port)
websocket_address = "ws://"+IPAddress+":"+server_port + "/websocket"
print("The server has this address: " + websocket_address)

# PLANNING CONSTANTS
algorithm_name= "ehs"
heuristic_name= "landmark"


class MyTimer:
    def __init__(self, timeout_duration):
        self.timeout_duration = timeout_duration
        self.timer = None 
        print("Timers have been set to wait for " + str(self.timeout_duration) +" seconds")

    def timeout_handler(self):
        print("\nTIME OVER!")
        ## DECIDERE COSA DEVE FARE PEPPER 

    def start(self): 
        self.timer = Timer(self.timeout_duration, self.timeout_handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()
        self.timer = None 


user_input = None
input_lock = threading.Lock()

def my_input(text, client):
    global user_input
    local_input = None
    while True:
        time.sleep(1)
        if client.stop_questions:
            print("The player touched the button.")
            break
        local_input = raw_input("INPUT in another thread: " + text)
        if local_input:
            with input_lock:
                user_input = local_input
            break

def input_thread(text, client):
    global user_input
    thread = threading.Thread(target=my_input, args=(text,client))
    thread.start()
    thread.join(timeout=10)
    return user_input
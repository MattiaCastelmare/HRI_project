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
import sys
import select


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
        # CHE FA PEPPER ?

    def start(self): 
        self.timer = Timer(self.timeout_duration, self.timeout_handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()
        self.timer = None 


def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()

    ready, _, _ = select.select([sys.stdin], [], [], timeout)

    if ready:
        return sys.stdin.readline().strip()
    else:
        return None


user_input = None
input_lock = threading.Lock()
stop_flag=True

def my_input(text, client):
    global user_input, stop_flag
    local_input = None
    stop_flag=True
    while stop_flag:
        
        time.sleep(1)
        if client.stop_questions:
            print("The player touched the button.")
            break
        local_input = input_with_timeout("INPUT in another thread: " + text,10)
        if local_input:
            with input_lock:
                user_input = local_input
            break

    return

def input_thread(text, client):
    global user_input,stop_flag
    thread = threading.Thread(target=my_input, args=(text,client))
    #thread.daemon = True
    thread.start()
    thread.setName('questionThread')
    thread.join(timeout=10)

    if thread.is_alive():
       stop_flag=False
       #thread._Thread__stop()  
       return user_input, True
    else:
        return user_input, False
    

#prova per vedere numeri thread
def print_active_threads():
    print("Active threads:", threading.active_count())
    print("Thread IDs:", threading.enumerate())




#description = 
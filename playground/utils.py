import tornado.ioloop
import random
import re
#import tornado.web
import tornado.websocket
import socket
#import tornado.gen

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
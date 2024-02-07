import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*
from client import*
sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
import pepper_cmd
from pepper_cmd import *

def main():
    begin()
    pepper_cmd.robot.say('Hello')
    # Create an event loop.
    io_loop = tornado.ioloop.IOLoop.current()
    # Before starting the event loop, instantiate a WebSocketClient and add a
    # callback to the event loop to start it. This way the first thing the
    # event loop does is to start the client.
    client = PepperClient(io_loop)
    io_loop.add_callback(client.start)
    # Send an example message, per farlo devi creare una funzione(callback)
    #io_loop.add_callback(client.send_message_from_client("I am listening send me a puzzle"))
    # Start the event loop.
    io_loop.start()
    #end()

if __name__ == "__main__":
    main()

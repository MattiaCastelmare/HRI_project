import sys
sys.path.append('/home/robot/playground')
from utils import*

@tornado.gen.coroutine
def main():

    begin()

    pepper_cmd.robot.say('Hello')

    # Create an HTTPRequest object
    request = HTTPRequest(url=websocket_address)

    # Create a WebSocket connection
    ws = yield tornado.websocket.websocket_connect(request)

    # Print a debug statement indicating successful connection
    print("WebSocket connection established.")

    # Send a message to the server
    ws.write_message("Hello from Pepper!")

    # Close the WebSocket connection
    ws.close()

    end()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)

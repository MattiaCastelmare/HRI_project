import sys
sys.path.append('/home/robot/playground')
from utils import*

class WebSocketClient(tornado.websocket.WebSocketClientConnection):
    def on_message(self, message):
        print("Received message from server: " + message)

@tornado.gen.coroutine
def main():
    # Replace 'your_server_ip' with the actual IP address of your WebSocket server
    websocket_address = websocket_address

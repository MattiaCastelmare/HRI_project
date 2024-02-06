import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*

class PepperClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        #self.num_successes = 0
        #self.num_trials = 0

    def start(self):
        self.connect_and_read()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        print("Connecting to " + websocket_address+ " ...")
        tornado.websocket.websocket_connect(
            url=websocket_address,
            callback=self.maybe_retry_connection,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )

    def maybe_retry_connection(self, future):
        try:
            self.connection = future.result()
            self.send_message_from_client("Hello from Pepper Robot!")
        except:
            print("Could not reconnect, retrying in 3 seconds...")
            self.io_loop.call_later(3, self.connect_and_read)

    def on_message(self, message):
        if message is None:
            print("Disconnected, reconnecting...")
            self.connect_and_read()
        else:
            print("Received from Server: ", message)

    def send_message_from_client(self, message):
        if self.connection:
            self.connection.write_message(message)
            print("Sent to the Server: ", message)
        else:
            print("Client not connected.")
import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*
from main import*
from motion import*

class PepperClient:
    def __init__(self, io_loop, session, tts_service):
        self.connection = None
        self.io_loop = io_loop
        # Set up a periodic callback every 5 seconds to send random numbers
        # self.periodic_callback = tornado.ioloop.PeriodicCallback(self.send_random_numbers, 5000)
        self.name = "/Pepper"
        self.session = session
        self.tts_service = tts_service

    def start(self):
        self.connect_and_read()
        #self.periodic_callback.start()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        print("Connecting to " + websocket_address + " ...")
        tornado.websocket.websocket_connect(
            url=websocket_address + self.name,
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
            if message.startswith("Game started"):
                difficulty = ask_questions(self.session, self.tts_service)
                print("THE DIFFICULTY IS ", difficulty)
                self.send_difficulty_to_server(difficulty)

    def send_message_from_client(self, message):
        if self.connection:
            self.connection.write_message(message)
            print("Sent to the Server: ", message)
        else:
            print("Client not connected.")

    def send_random_numbers(self):
        # Send two random numbers between 0 and 8 every 5 seconds
        random_numbers = [random.randint(0, 8) for _ in range(2)]
        message = "PepperMove: {}".format(','.join(map(str, random_numbers)))
        self.send_message_from_client(message)
    #@classmethod
    def send_difficulty_to_server(self, difficulty):
        # Method to send difficulty level chosen by the user to the server
        message = "Difficulty: {}".format(difficulty)
        self.send_message_from_client(message)
        
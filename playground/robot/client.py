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
        self.name = "/Pepper"
        self.session = session
        self.tts_service = tts_service
        self.stop_questions = False
  
    def start(self):
        self.connect_and_read()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        print("\nCLIENT THREAD: Connecting to " + websocket_address + " ...")
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
            self.send_message_from_client("Hello from Pepper Client!")
        except:
            print("CLIENT THREAD: Could not reconnect, retrying in 3 seconds...")
            self.io_loop.call_later(3, self.connect_and_read)

    def on_message(self, message):
        if message is None:
            print("Message is empty")
            self.connect_and_read()
        else:
            print("CLIENT THREAD: Received from Server: ", message)
            if message.startswith("User made 3"):
                makes_move_for_you(self.session, self.tts_service)
                answer = raw_input("Enter your answer (yes, no): ")
                self.send_answer_to_server(answer)
                
            if message.startswith("Button pressed"):
                self.stop_questions = True
                
    def send_message_from_client(self, message):
        if self.connection:
            self.connection.write_message(message)
            print("CLIENT THREAD: Sent to the Server: " + message)
        else:
            print("Could not send message")

    def send_random_numbers(self):
        # Send two random numbers between 0 and 8 every 5 seconds
        random_numbers = [random.randint(0, 8) for _ in range(2)]
        message = "PepperMove: {}".format(','.join(map(str, random_numbers)))
        self.send_message_from_client(message)

    def send_difficulty_to_server(self, difficulty):
        # Method to send difficulty level chosen by the user to the server
        message = "Difficulty: {}".format(difficulty)
        self.send_message_from_client(message)

    def send_answer_to_server(self, answer):
        # Method to send difficulty level chosen by the user to the server
        message = "Answer is: {}".format(answer.lower())
        self.send_message_from_client(message)

        

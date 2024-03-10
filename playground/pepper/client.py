import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*
from main import*
from motion import*

################################################## PEPPER CLIENT CLASS #######################################################
class ClientPepper:
    def __init__(self, io_loop):
        # WebSocket connection object
        self.connection = None
        # Tornado I/O loop
        self.io_loop = io_loop
        # Client name
        self.name = "/Pepper"
        # Flag to stop questions
        self.stop_questions = False
        # Flag indicating the win condition
        self.win_flag = False
        # Name of the current painting
        self.painting_name = None
        # Save pepperRobot class
        self.pepperRobot = None

    # INITIALIZE CLIENT
    def start(self):
        self.connect_and_read()

    # STOPS CLIENT
    def stop(self):
        print("Stopping I/O loop...")
        self.io_loop.add_callback(self.io_loop.stop)
        #self.io_loop.stop()
        #self.io_loop.close()

    # INITIALIZES CONNECTION
    def connect_and_read(self):
        print("\nCLIENT THREAD: Connecting to " + websocket_address + " ...")
        tornado.websocket.websocket_connect(
            url=websocket_address + self.name,
            callback=self.maybe_retry_connection,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )

    # RETRIES IF CONNECTION IS UNSUCCLESSFUL
    def maybe_retry_connection(self, future):
        try:
            self.connection = future.result()
            self.send_message_from_client("Hello from Pepper Client!")
        except:
            print("\nCLIENT THREAD: Could not reconnect, retrying in 3 seconds...")
            self.io_loop.call_later(3, self.connect_and_read)

    
    # RETRIEVE THE ROBOT CLASS
    def get_robot(self, robotClass):
        self.pepperRobot = robotClass

    # INCOMING MESSAGES
    def on_message(self, message):
        # Handles case where the message is empty.
        if message is None:
            print("\nCLIENT THREAD: Message is empty")
            self.connect_and_read()
        else:
            print("\nCLIENT THREAD: Received from Server: " +  message)
            if message.startswith("User made 3"):
                self.pepperRobot.makes_move_for_you()
                answer = input_with_timeout("(HELP) Enter your answer (yes, no): ", timeout)
                if answer:
                    self.send_answer_to_server(answer)
            if message == "Button pressed":
                self.stop_questions = True
            if message == "Win":
                self.win_flag = True
            if message == "Game started":
                # Reinitializes the win flag on the client side.
                self.win_flag = False
            if message.startswith("Painting name"):
                # Extracts and sets the current painting name from the message.
                self.painting_name = message.replace("Painting name:", "").replace(".jpg", "")
            if message.startswith("Uncorrect"):
                self.pepperRobot.bad_move()
            if message.startswith("Correct"):
                self.pepperRobot.cheer_move()

    # SEND MESSAGE FROM CLIENT TO SERVER
    def send_message_from_client(self, message):
        if self.connection:
            self.connection.write_message(message)
            print("\nCLIENT THREAD: Sent to the Server: " + message)
        else:
            print("Could not send message")

    # Sends the user's answer to the server.
    # Parameters:
    # - answer: User's input (yes or no) to be sent to the server.
    def send_answer_to_server(self, answer):
        message = "Answer is: {}".format(answer.lower())
        self.send_message_from_client(message)
#############################################################################################################################

############################ INITIALIZES PEPPER CLIENT AND STARTS IO_LOOP ###################################################
def start_client(event):
    global pepperClient
    io_loop = tornado.ioloop.IOLoop.current()
    pepperClient = ClientPepper(io_loop=io_loop)
    io_loop.add_callback(pepperClient.start)
    # After the initialization set the timer
    event.set()
    io_loop.start()

############################# CONNECT TO SERVER IN ANOTHER THREAD #############################################################
def connect_to_server():
    event = threading.Event()
    ws_thread = threading.Thread(target=start_client, args=(event,))
    ws_thread.daemon = True
    ws_thread.setName("ClientThread")
    ws_thread.start()
    # Wait for the client to start correctly before continuing in the main thread
    event.wait()
    return pepperClient

###############################################################################################################################


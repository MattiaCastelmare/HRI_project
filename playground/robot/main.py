import qi
import os
import sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*
from client import*

sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
import pepper_cmd
from pepper_cmd import*
from motion import*

def sentences(index):
    sentence = [
        "Hello, I'm a playful robot, nice to meet you. I have some puzzles to solve, do you want to help me?",
        "Great! Let's play together. Before starting the game I want to ask you some questions about you",
        "How old are you?",
        "Do you like logic problems? ",
        "According to what you have said I have chosen the easy level jigsaw puzzle for you",
        "According to what you have said I have chosen the medium level jigsaw puzzle for you",
        "According to what you have said I have chosen the hard level jigsaw puzzle for you",
        "This move is incorrect, can I help you?",
        "This move is correct, great!",
        "You made 3 incorrect moves let me to help you by doing 2 correct moves",
        "You have completed the jigsaw puzzle, congratulation!",
    ]
    return sentence[index]

def difficulties(index):
    difficulty = [
            "easy",
            "medium",
            "hard" 
        ]
    return difficulty[index]

def initialize_robot():
    pip = os.getenv('PEPPER_IP')

    pport = 9559

    url = "tcp://" + pip + ":" + str(pport)

    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session 

    tts_service = session.service("ALAnimatedSpeech")
    configuration = {"bodyLanguageMode":"disabled"} 

    return session, tts_service

def main():

    #begin()
    # Create an event loop.
                
    io_loop = tornado.ioloop.IOLoop.current()

    client = PepperClient(io_loop)
  
    io_loop.add_callback(client.start)
    

    # Send an example message, per farlo devi creare una funzione(callback)
    #io_loop.add_callback(client.send_message_from_client("I am listening send me a puzzle"))

    # Start the event loop.
    io_loop.start()
   
    # #end()

    """ Structure of the main
    1) Start the client connecting to the server
    2) Start the robot interacting with the user asking questions
    3) According to the answers choose a puzzle
    4) The user interacts with the puzzle and make moves
    5) Robot interacts witht the user telling him if the moving he is making is correct or not
    6) After 2 uncorrect moves the robot plays the move
    7) The puzzle is terminated   
    """

    return 
def quiz():

    ##begin()
    session, tts_service = initialize_robot()
    initial_sentence = sentences(0)
    #move_talk(robot = session, text = initial_sentence, char = "greeting", service = tts_service)
    answer = raw_input("Enter your answer: (yes or no)")

    if answer.lower() == "no":
        end()

    if answer.lower() == "yes":
        introduction_sentence = sentences(1)
        #move_talk(robot = session, text = introduction_sentence, char = "talk1", service = tts_service)

        age_question = sentences(2)
        #move_talk(robot = session, text = age_question, char = "talk1", service = tts_service)
        age = raw_input("Enter you age in number: ")

        logic_puzzle_question = sentences(3)
        #move_talk(robot = session, text = logic_puzzle_question, char = "talk1", service = tts_service)
        attitude_to_logic = raw_input("Enter your answer: (yes or no or not so much)")


        if age < 10:
            if (attitude_to_logic.lower() == "no" or attitude_to_logic.lower() == "not so much"):
                difficulty = difficulties(0)

            if attitude_to_logic.lower() == "yes":
                difficulty = difficulties(1)
        if 10 <= age <= 18:
            if (attitude_to_logic.lower() == "no" or attitude_to_logic.lower() == "not so much"):
                difficulty = difficulties(1)

            if attitude_to_logic.lower() == "yes":
                difficulty = difficulties(2)
        
        if age > 18:
            if (attitude_to_logic.lower() == "no" or attitude_to_logic.lower() == "not so much"):
                difficulty = difficulties(1)

            if attitude_to_logic.lower() == "yes":
                difficulty = difficulties(2)
    return difficulty

if __name__ == "__main__":
    main()
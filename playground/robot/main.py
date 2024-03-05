import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*
from client import*

sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
import pepper_cmd
from pepper_cmd import*
from motion import*

# HUMAN ROBOT INTERACTION SIMULATION
class Robot:
    def __init__(self):
        self.flag = None
        self.thread = None
        self.task = None

    def _activity(self, task):
        while self.flag:
            print("ROBOT THREAD: Pepper is " + task)
            time.sleep(5)

    def start_activity(self,task):
        self.flag = True
        self.task = task
        self.thread = threading.Thread(target=self._activity, args=(task,))
        if task == "waiting":
            self.thread.daemon = True
        self.thread.start()

    def stop_activity(self):
        self.flag = False
        if self.task == "waiting":
            print("ROBOT THREAD: Human Approached")
        elif self.task == "playing":
            print("ROBOT THREAD: Pepper stopped playing")
        

puzzle_completed = True
sequence_incorrect = True
clientPepper = None
timer = MyTimer(20)
pepperRobot = Robot()

def start_client(session, tts_service):
    global clientPepper
    io_loop = tornado.ioloop.IOLoop.current()
    clientPepper = PepperClient(io_loop=io_loop, session=session, tts_service=tts_service)
    io_loop.add_callback(clientPepper.start)
    io_loop.start()
    
def questionaire(client, tts_service, session):
    introduction_sentence = sentences(1)
    move_talk(robot=session, text=introduction_sentence, char="talk", service=tts_service)
    
    age_question = sentences(2)
    move_talk(robot=session, text=age_question, char=" ", service=tts_service)
    #age = raw_input("INPUT: Enter your age in number: ")
    age = input_thread("Enter your age in number: ", client)
    print(age)

    logic_puzzle_question = sentences(3)
    move_talk(robot=session, text=logic_puzzle_question, char="talk", service=tts_service)
    #attitude_to_logic = raw_input("INPUT: Enter your answer(yes, no, not so much): ")
    attitude_to_logic = input_thread("Enter your answer(yes, no, not so much): ", client)

    if age and attitude_to_logic:
        if age < 10:
            difficulty = difficulties(0) if attitude_to_logic.lower() in ["no", "not so much"] else difficulties(1)
        elif 10 <= age <= 18:
            difficulty = difficulties(1) if attitude_to_logic.lower() in ["no", "not so much"] else difficulties(2)
        else:
            difficulty = difficulties(1) if attitude_to_logic.lower() in ["no", "not so much"] else difficulties(2)
        return difficulty
    else: 
        return None
    

def simulation(session,tts_service):
    global pepperRobot
    # Pepper is idle and waits 
    pepperRobot.start_activity("waiting")

    # Simulating human approaches
    user_input = raw_input("\nINPUT: Enter 'stop' to approach the robot: ")
    if user_input == 'stop': 
        pepperRobot.stop_activity()
    
    print("\nMAIN: Waiting 1 sec ... ")
    time.sleep(1)

    # Pepper greets and asks to play
    timer.start()
    user_input = raw_input("\nDo you want to play? (yes, no) ")
    timer.stop()
    if user_input and user_input.lower() == "yes":
        print("MAIN: Human wants to play")
        clientPepper.send_message_from_client("User wants to play")
        return
    else:
        print("\nMAIN: Human doesn't want to play")
        goodbye_and_talk(session=session, tts_service=tts_service)
        simulation(session=session, tts_service=tts_service)
    

def main():
    # Initialize Pepper Robot
    session, tts_service = initialize_robot()
    print("\nMAIN: Waiting 1 sec ... ")
    time.sleep(1)
    
    # Connect to the Server in another thread
    ws_thread = threading.Thread(target=start_client, args=(session,tts_service))
    ws_thread.daemon = True
    ws_thread.start()
   
    simulation(session=session, tts_service= tts_service)
    
    print("\nMAIN: Waiting 1 sec ... ")
    time.sleep(1)

    # Pepper does questionnaire to decide difficulty of the puzzle
    difficulty = questionaire(clientPepper,  tts_service=tts_service, session=session)
    
    if difficulty:
        clientPepper.send_message_from_client("The suggested difficulty is:" + difficulty)
        suggest_difficulty(session=session, tts_service=tts_service, difficulty=difficulty)
        pepperRobot.start_activity("playing") ## DA QUI NON ESC QUINDI TROVARE MODO DI FARLO USCIRE, BISOGNA PENSARCI E DECIDERLO INSIEME
    else:
        print("The user did not answer all the questions")
        ## Questo quando scade timeout delle domande o quando arriva il mex
        ### FARE DUE CASI DIVERSI
        

if __name__ == "__main__":
    main()
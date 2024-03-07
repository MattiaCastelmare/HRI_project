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
            time.sleep(8)

    def start_activity(self,task):
        self.flag = True
        self.task = task
        self.thread = threading.Thread(target=self._activity, args=(task,))
        self.thread.setName("RobotThread")
        if task == "waiting":
            self.thread.daemon = True
        self.thread.start()

    def stop_activity(self):
        self.flag = False
        self.thread = None
        if self.task == "waiting":
            print("ROBOT THREAD: Human Approached")
        elif self.task == "playing":
            print("ROBOT THREAD: Pepper stopped playing")
        

puzzle_completed = True
sequence_incorrect = True
clientPepper = None
timer = MyTimer(10)
pepperRobot = Robot()
painting_name = None
age = None

def start_client(session, tts_service):
    global clientPepper
    io_loop = tornado.ioloop.IOLoop.current()
    clientPepper = PepperClient(io_loop=io_loop, session=session, tts_service=tts_service)
    io_loop.add_callback(clientPepper.start)
    io_loop.start()
    

def simulation(session,tts_service):
    global pepperRobot
    # Pepper is idle and waits 
    pepperRobot.start_activity("waiting")
    #print_active_threads()
    # Simulating human approaches
    user_input = raw_input("\nINPUT: Enter 'stop' to approach the robot: ")
    print(user_input)
    if user_input == 'stop': 
        pepperRobot.stop_activity()
        greeting(session, tts_service)
    
    #print("\nMAIN: Waiting 1 sec ... ")
    #time.sleep(1)

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
        print("\nMAIN: Waiting 1 sec ... ")
        time.sleep(1)
        goodbye_and_talk(session=session, tts_service=tts_service)
        simulation(session=session, tts_service=tts_service)

def get_painting_text(age):
    global painting_name
    # Get the painting name from the client
    painting_name = clientPepper.painting_name
    if painting_name:
        if age:
            if age<12:
                painting_text = paintings_info[painting_name]['children']
            if age<12:
                painting_text = paintings_info[painting_name]['adults']
        else:
            painting_text = paintings_info[painting_name]['children']
        print("Painting name is: " + painting_name)
        return painting_text
    else:
        print("The painting name has not been correctly been given")


def puzzle_completed(robot, session, service):
    global age
    # STOPS PLAYING
    robot.stop_activity()
    # GET PAINTING DESCRIPTION 
    painting_text = get_painting_text(age)
    # FINAL DANCE and TALKS ABOUT THE PAINTING
    final(description=painting_text, session=session, tts_service= service)
    # ASKS USER IF HE WANTS TO PLAY AGAIN
    play_again = input_with_timeout("Enter yes to play again",10)
    if play_again.lower() == "yes":
        # GO BACK TO THE CHOOSEN DIFFICULTY SCHERMATA
        clientPepper.send_message_from_client("Play again")
        # Controlla se ha vinto
        check_win(session=session, tts_service= service)
    else:
        # GO BACK TO WAITING (INITIAL STATE)
        clientPepper.send_message_from_client("Exit")
        clientPepper.stop_questions = False
        clientPepper.win_flag = False
        run(session, service)

def check_win(session, tts_service):
    while not clientPepper.win_flag:
            time.sleep(1)
    clientPepper.win_flag = False
    puzzle_completed(pepperRobot, session, tts_service)


def run(session, tts_service):
    simulation(session=session, tts_service= tts_service)
    
    print("\nMAIN: Waiting 1 sec ... ")
    time.sleep(1)

    # Pepper does questionnaire to decide difficulty of the puzzle
    difficulty = questionaire(clientPepper,tts_service=tts_service, session=session)
    
    if difficulty and not clientPepper.stop_questions:
        # ANSWERED ALL QUESTIONS
        clientPepper.send_message_from_client("The suggested difficulty is:" + difficulty)
        suggest_difficulty(session=session, tts_service=tts_service, difficulty=difficulty)
        pepperRobot.start_activity("playing")
        check_win(session=session, tts_service= tts_service)
    if  not difficulty and not clientPepper.stop_questions:
        # TIMER SCADUTO
        print("The user did not answer all the questions, so we assume they left")
        run(session=session, tts_service= tts_service)
    if not difficulty and clientPepper.stop_questions:
        # PLAY BUTTON PRESSED
        print("The user did not answer all the questions but the play button was pressed")
        pepperRobot.start_activity("playing")
        check_win(session=session, tts_service= tts_service)
    else:
        print("There is something wrong")
        sys.exit()

def main():
    # Initialize Pepper Robot
    session, tts_service = initialize_robot()
    print("\nMAIN: Waiting 1 sec ... ")
    time.sleep(1)
    
    # Connect to the Server in another thread
    ws_thread = threading.Thread(target=start_client, args=(session,tts_service))
    ws_thread.daemon = True
    ws_thread.setName("ClientThread")
    ws_thread.start()
    
    print(1)
    run(session=session, tts_service = tts_service)

        

if __name__ == "__main__":
    main()
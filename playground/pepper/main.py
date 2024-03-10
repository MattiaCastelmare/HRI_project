import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
from utils import*
from motion import*
from robot import *
from client import *

############################################ GLOBAL VARIABLES ###########################################################    
painting_name = None
age = None
pepperRobot = None
pepperClient = None

############################################ MAIN #####################################################################
def main():
    global pepperRobot, pepperClient, client_thread
    # INITIALIZE PEPPER SIMULATION 
    session, tts_service = initialize_robot()
    
    # CONNECT TO SERVER ON A NEW THREAD
    pepperClient = connect_to_server()

    # INITIALIZE ROBOT CLASS, RUNS IN ROBOT AND MAIN THREAD & PASS IT TO THE CLIENT
    pepperRobot = RobotPepper(pepperClient, session, tts_service)
    pepperClient.get_robot(pepperRobot)
    
    # APPROACH & QUESTIONS & DIFFICULTY
    initial_interaction()

############################################ INITIAL INTERACTION #####################################################################
def initial_interaction():
    # APPROACH SIMULATION
    approach_simulation()

    # PEPPER ASKS SOME QUESTIONS
    difficulty = pepperRobot.questionaire()
    
    # ANSWERED ALL QUESTIONS
    if difficulty and not pepperClient.stop_questions:
        pepperClient.send_message_from_client("The suggested difficulty is:" + difficulty)
        pepperRobot.suggest_difficulty(difficulty=difficulty)
        pepperRobot.show_tablet()
        pepperRobot.stop_activity()
        pepperRobot.start_activity("playing")
        check_win()
    # TIMER SCADUTO
    if  not difficulty and not pepperClient.stop_questions:
        pepperClient.send_message_from_client("Go back waiting")
        pepperRobot.stop_activity()
        print("The user did not answer all the questions, so we assume they left")
        initial_interaction()
    # PLAY BUTTON PRESSED
    if not difficulty and pepperClient.stop_questions:
        print("The user did not answer all the questions but the play button was pressed")
        pepperRobot.show_tablet()
        pepperRobot.stop_activity()
        pepperRobot.start_activity("playing")
        check_win()
    else:
        print("There is something wrong")
        sys.exit()

###################################### SIMULATE HUMAN COMING NEAR PEPPER ###############################################
def approach_simulation():
    # PEPPER IDLE  
    pepperRobot.start_activity("waiting")
    # HUMAN APPROACHES SIMULATED
    user_input = raw_input("\nMAIN: Enter something to approach the robot: ")
    if user_input: 
        pepperRobot.stop_activity()
        pepperRobot.greeting()
    # PEPPER ASKS IF THEY WANT TO PLAY
    user_input = input_with_timeout("\nMAIN: Enter yes to play (yes, no) ", timeout)
    # HUMAN WANTS TO PLAY
    if user_input and user_input.lower() == "yes":
        print("\nMAIN: Human wants to play")
        pepperRobot.stop_activity()
        pepperClient.send_message_from_client("User wants to play")
        return
    # HUMAN DOESN'T WANT TO PLAY
    if user_input and user_input.lower() == "no":
        print("\nMAIN: Human doesn't want to play")
        pepperRobot.stop_activity()
        pepperRobot.goodbye_and_talk()
        approach_simulation()
    # HUMAN DID NOT ANSWER, GO BACK TO WAITING
    else:
        print("\nMAIN: Human didn't answer or Answer not accepted")
        pepperRobot.stop_activity()
        approach_simulation()

############################################ CONTINUOS CHECK ############################################################
def check_win():
    # While the flag is false wait, when it becomes true run the victory scenario
    while not pepperClient.win_flag:
            time.sleep(1)
    pepperClient.win_flag = False
    puzzle_completed()

######################################### RETRIVE PAINTING DESCRIPTION ##################################################
def get_painting_text(age):
    # Get the painting name from the client
    painting_name = pepperClient.painting_name
    if painting_name:
        if age:
            if age<12:
                painting_text = paintings_info[painting_name]['children']
            if age<12:
                painting_text = paintings_info[painting_name]['adults']
        else:
            painting_text = paintings_info[painting_name]['children']
        print("\nMAIN: Painting name is: " + painting_name)
        return painting_text
    else:
        print("\nMAIN: The painting name has not been correctly been given")

#################################### WIN SCENARIO ######################################################################
def puzzle_completed():
    # STOPS PLAYING
    pepperRobot.stop_activity()
    # GET PAINTING DESCRIPTION 
    painting_text = get_painting_text(age)
    # FINAL DANCE & TALKS ABOUT THE PAINTING
    pepperRobot.final(description=painting_text)
    # ASKS USER IF HE WANTS TO PLAY AGAIN
    play_again = input_with_timeout("\nMAIN: Enter yes to play again: (yes, no): ",  timeout)
    if play_again and play_again.lower() == "yes":
        # GO BACK TO THE CHOOSEN DIFFICULTY SCHERMATA
        pepperClient.send_message_from_client("Play again")
        check_win()
    else:
        # GO BACK TO WAITING (INITIAL STATE)
        pepperClient.send_message_from_client("Exit")
        pepperClient.stop_questions = False
        pepperClient.win_flag = False
        initial_interaction()


################################################### RUN #################################################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Main Thread Keyboard Interrupt ...")
        pepperClient.stop()

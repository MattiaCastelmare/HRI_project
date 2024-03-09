import os, sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from pepper_cmd import *
from utils import *
from motion import *

############################################ ROBOT CLASS  #########################################################
class RobotPepper:
    def __init__(self, client, session, tts_service):
        self.flag = None
        self.thread = None
        self.task = None
        self.session= session
        self.tts_service = tts_service
        self.client = client

    # GREETS AND ASK YOU IF YOU WANT TO PLAY 
    def greeting(self):
        sentence = sentences(0)
        move_talk(robot=self.session, text=sentence, char="greeting", service=self.tts_service)

    # QUESTIONNARIE ABOUT THE DIFFICULTY TO SUGGEST 
    def questionaire(self):
        global age
        introduction_sentence = sentences(1)
        move_talk(robot=self.session, text=introduction_sentence, char="talk", service=self.tts_service)
        if not self.client.stop_questions:
            age_question = sentences(2)
            move_talk(robot=self.session, text=age_question, char=" ", service=self.tts_service)
            age = input_with_timeout("Enter your age in number: ", timeout)
            if not age:
                return None
        else:
            return None
        if not self.client.stop_questions:
            logic_puzzle_question = sentences(3)
            move_talk(robot=self.session, text=logic_puzzle_question, char="new talk", service=self.tts_service)
            attitude_to_logic =input_with_timeout("Enter your answer (1,2,3,4,5): ", timeout)
            if not attitude_to_logic:
                return None
        else:
            return None
        if not self.client.stop_questions:
            patience = sentences(4)
            move_talk(robot=self.session, text=patience, char="talk", service=self.tts_service)
            how_much_patience = input_with_timeout("Enter your answer (little, enough, a lot): ", timeout)
            if not how_much_patience:
                return None
        else:
            return None
        if not self.client.stop_questions:
            art = sentences(5)
            move_talk(robot=self.session, text=art, char = "", service=self.tts_service)
            like_art = input_with_timeout("Enter you anser (little, enough, a lot): ", timeout)
            if not like_art:
                return None
        else:
            return None
        age=int(age)
        attitude_to_logic=int(attitude_to_logic)
        if age < 10 and attitude_to_logic <= 4 and how_much_patience.lower() in ["little", "enough"] and like_art.lower() in ["little", "enough"]:
            difficulty = difficulties(0)
        elif age < 10 and attitude_to_logic > 4 and how_much_patience.lower() in ["enough", "a lot"] and like_art.lower() in ["enough", "a lot"]:
            difficulty = difficulties(1)
        elif 10 <= age <= 18 and attitude_to_logic <= 3 and how_much_patience.lower() in ["little", "enough"] and like_art.lower() in ["little"]:
            difficulty = difficulties(0)
        elif 10 <= age <= 18 and 3 <= attitude_to_logic <= 4 and how_much_patience.lower() in ["enough", "a lot"] and like_art.lower() in ["enough", "a lot"]:
            difficulty = difficulties(1)
        elif 10 <= age <= 18 and attitude_to_logic == 5 and how_much_patience.lower() in ["a lot"] and like_art.lower() in ["a lot"]:
            difficulty = difficulties(2)
        elif age > 18 and attitude_to_logic <= 3 and how_much_patience.lower() in ["little", "enough"] and like_art.lower() in ["little", "enough"] :
            difficulty = difficulties(1)
        elif age > 18 and attitude_to_logic > 3 and how_much_patience.lower() in ["enough", "a lot"] and like_art.lower() in ["enough", "a lot"]:
            difficulty = difficulties(2)
        else:
            difficulty = difficulties(1)
        return difficulty

    # PEPPER MOVES AND SUGGEST YOU THE DIFFICULTY BASED ON THE QUESTIONNAIRE 
    def suggest_difficulty(self,difficulty):
        difficulty_sentences = {
            "easy": 6,
            "medium": 7,
            "hard": 8
        }
        sentence_index = difficulty_sentences.get(difficulty.lower())
        if sentence_index is not None:
            sentence = sentences(sentence_index)
            move_talk(robot=self.session, text=sentence, char="new talk", service=self.tts_service)

    # PEPPER SHOWS THE TABLET WITH THE PUZZLE 
    def show_tablet(self):
        sentence = sentences(12)
        move_talk(robot=self.session, text=sentence, char="show", service=self.tts_service)

    # PEPPER SAYS THAT YOU MADE 3 ERRORS AND MAKES 2 MOVE FOR YOU    
    def makes_move_for_you(self):
        sentence = sentences(9)
        move_talk(robot=self.session, text=sentence, char="talk", service=self.tts_service)

    # PEPPER CHEERS FOR YOUR CORRECT MOVE 
    def cheer_move(self):
        sentence = good_sentences()
        char = "good move"
        random_number = random.random()
        if random_number > 0.7:
            char = " "
        move_talk(robot=self.session, text=sentence, char=char, service=self.tts_service)

    # PEPPER TELLS YOU INCORRECT MOVE 
    def bad_move(self):
        sentence = bad_sentences()
        char = "bad move"
        move_talk(robot=self.session, text=sentence, char=char, service=self.tts_service)

    # PEPPER MAKES THE FINAL DANCE TO CELEBRATE THE VICTORY    
    def final(self,description):
        sentence = sentences(10)
        move_talk(robot=self.session, text=sentence, char="final dance", service=self.tts_service)
        move_talk(robot=self.session, text=description, char="new talk", service=self.tts_service)

    # PEPPER SAYS GOODBYE AT THE END OF THE GAME 
    def goodbye_and_talk(self):
        sentence = sentences(11)
        move_talk(robot=self.session, text=sentence, char="goodbye", service=self.tts_service)

    # RUN CONTINUOSLY GENERAL ACTIVITY UNTIL FLAG ( SIMULATION )
    def _activity(self, task):
        while self.flag:
            print("\nROBOT THREAD: Pepper is " + task)
            time.sleep(8)

    # START GENERAL ACTIVITY RUN
    def start_activity(self,task):
        print("\nROBOT THREAD: Pepper starts " + task)
        self.flag = True
        self.task = task
        self.thread = threading.Thread(target=self._activity, args=(task,))
        self.thread.setName("RobotThread")
        if task == "waiting":
            self.thread.daemon = True
        self.thread.start()

    # STOPS GENERAL ACTIVITY RUN
    def stop_activity(self):
        self.flag = False
        self.thread = None
        if self.task == "waiting":
            print("\nROBOT THREAD: Human Approached")
        elif self.task == "playing":
            print("\nROBOT THREAD: Pepper stopped playing")

##############################################################################################################################
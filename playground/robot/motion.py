""" 
Implementation of the speech of Pepper and its motion
"""

import qi
import os 
import sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
import pepper_cmd
from pepper_cmd import *
import time
from utils import *

# LOOK ACTION 
def look(robot, direction):
    session = robot.service("ALMotion")
    jointNames = ["HeadYaw", "HeadPitch"]
    isAbsolute = True
    if direction == "left":
        initAngles = [0.5, -0.2]
        timeLists  = [1.0, 1.0]       
        session.angleInterpolation(jointNames, initAngles, timeLists, isAbsolute)
    if direction == "right":
        finalAngles = [-0.5, -0.2]
        timeLists  = [1.0, 1.0]
        session.angleInterpolation(jointNames, finalAngles, timeLists, isAbsolute)
    return

# SAYING NO
def no_with_head(robot):
    look(robot, "left")
    look(robot, "right")
    return

# RAISE ARM
def raiseArm(robot, which='R'): # or 'R'/'L' for right/left arm
    session = robot.service("ALMotion")
    if (which=='R'):
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        jointValues = [ -1.0, -0.3, 1.22, 0.52, -1.08] 
    else:
        jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        jointValues = [ 1.5, 0.3, 0.0, 0.2, 0.0] 
    times = [1.0, 1.0, 1.0, 1.0, 1.0]
    isAbsolute = True
    pause = 1 # how much time you want to keep the hand over the head
    for i in range(pause):
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    return

# RAISE ARM
def raiseArms(robot): 
    session = robot.service("ALMotion")
    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
                  "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
    jointValues = [ -1.0, -0.3, 1.22, 0.52, -1.08,
                     -1.0, -0.3, 1.22, 0.52, -1.08] 

    times = [1] * len(jointNames)
    isAbsolute = True
    pause = 3 # how much time you want to keep the hand over the head
    for i in range(pause):
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    return

# WAVING ARM
def waveArm(robot, which = "R"): 
    session = robot.service("ALMotion")
    if which == 'R':
        jointNames = ["RShoulderRoll"]
    else:
        jointNames = ["LShoulderRoll"]
    jointValues_right = [-0.5]
    jointValues_left = [0.5]
    isAbsolute = True
    time_waving = 0.5
    for i in range(5):
        if i % 2 == 0:
            session.angleInterpolation(jointNames, jointValues_right, time_waving, isAbsolute)
        else:
            session.angleInterpolation(jointNames, jointValues_left, time_waving, isAbsolute)
    return

# MOVE AND GREET
def move_greeting(robot):
  session = robot.service("ALMotion")
  isAbsolute = True
  jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch"]
  jointValues = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07]
  t = 1.0
  times  = [t, t, t, t, t, t, t]
  session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  for i in range(2):
    jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [2.7, -0.07, -0.07]
    times  = [0.6, 0.6, 0.6]
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [1.3, -0.07, -0.07]
    times  = [0.6, 0.6, 0.6]
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

  return


# # 1st STRANGE TALKING
# def talking1(robot):
#     session = robot.service("ALMotion")
#     isAbsolute = True
#     jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
#     jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]
#     t = 1.0
#     times  = [t] * len(jointNames)
#     session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#     for i in range(2):
#         jointNames = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
#         jointValues = [1.5, 1.0, -1.2]
#         times  = [0.6, 0.6, 0.6]
#         session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#         jointNames = ["LShoulderPitch", "LElbowRoll", "LWristYaw"]
#         jointValues = [1.5, -1.0, 1.2]
#         session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#     for i in range(2):
#         jointValues = [-0.141, 0.892, -0.8]
#         session.angleInterpolation(["RShoulderPitch", "RElbowRoll", "RWristYaw"], jointValues, times, isAbsolute)
#         jointValues = [-0.141, 0.892, -0.8]
#         session.angleInterpolation(["LShoulderPitch", "LElbowRoll", "LWristYaw"], jointValues, times, isAbsolute)
#     session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#     return

# # 2nd STRANGE TALKING
# def talking2(robot):
#     session = robot.service("ALMotion")
#     isAbsolute = True
#     jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
#     jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]
#     t = 1.0
#     times  = [t] * len(jointNames)
#     session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#     for i in range(2):
#         jointNames = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
#         jointValues = [1.5, 1.0, -1.2]
#         session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#         jointNames = ["LShoulderPitch", "LElbowRoll", "LWristYaw"]
#         jointValues = [1.5, -1.0, 1.2]
#         session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#         jointValues = [-0.141, 0.892, -0.8]
#         session.angleInterpolation(["RShoulderPitch", "RElbowRoll", "RWristYaw"], jointValues, times, isAbsolute)
#         jointValues = [-0.141, 0.892, -0.8]
#         session.angleInterpolation(["LShoulderPitch", "LElbowRoll", "LWristYaw"], jointValues, times, isAbsolute)
#     session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

#     return

# # 3rd STRANGE TALKING
# def talking3(robot):
#     session = robot.service("ALMotion")
#     isAbsolute = True
#     jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
#     jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]
#     t = 1.0
#     times = [t] * len(jointNames)
#     session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#     for i in range(2):
#         jointNames = ["RShoulderPitch", "LShoulderPitch", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw"]
#         jointValues_up = [1.5, 1.5, 1.0, -1.0, -1.2, 1.2]
#         session.angleInterpolation(jointNames, jointValues_up, times, isAbsolute)
#         jointValues_down = [-0.141, -0.141, 0.892, 0.892, -0.8, -0.8]
#         session.angleInterpolation(jointNames, jointValues_down, times, isAbsolute)
#     session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
#     return

# GOODBYE
def goodbye(robot):
    raiseArm(robot, "R")
    waveArm(robot, "R")
    return

def final_dance(robot):
    session = robot.service("ALMotion")
    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
    jointValues = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07, -0.141, 0.46, -0.892, 0.8, -0.98]
    times = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    isAbsolute = True
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    for i in range(2):
        # First set of arm and hip movements
        jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
        jointValues = [2.7, -1.3, -0.07, -0.07]
        times = [0.8, 0.8, 0.8, 0.8]
        isAbsolute = True
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

        # Second set of arm and hip movements
        jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
        jointValues = [1.3, -2.7, 0.07, -0.07]  # Adjusted HipRoll value for opposite movement
        times = [0.8, 0.8, 0.8, 0.8]
        isAbsolute = True
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    return


# DANCE
def dance(robot):
    session = robot.service("ALMotion")
    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
    jointValues = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07, -0.141, 0.46, -0.892, 0.8, -0.98]
    times  = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    isAbsolute = True
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    for i in range(2):
            jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
            jointValues = [2.7, -1.3, -0.07, -0.07]
            times  = [0.8, 0.8, 0.8, 0.8]
            isAbsolute = True
            session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
            jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
            jointValues = [1.3, -2.7, -0.07, -0.07]
            times  = [0.8, 0.8, 0.8, 0.8]
            isAbsolute = True
            session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
            return
    

# NORMAL TALK
def talk(robot, n_hands = 2):
    session = robot.service("ALMotion")
    isAbsolute = True
    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", 
                    "RHand", "HipRoll", "HeadPitch"]
    jointValues = [0.5, -0.46, 0.892, 1.5, 0.98, -0.07, -0.07]
    times  = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    times = [time*0.7 for time in times]
    if n_hands == 2:
        jointNames += ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
        jointValues += [0.5, 0.46, -0.892, -1.5, 0.98]
        times += [0.7 for i in range(5)]
    for i in range(2):  
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    
    jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [2.7, -0.07, -0.07]
    times  = [0.6, 0.6, 0.6]

    if n_hands == 2:
        jointNames.append("LElbowYaw")
        jointValues.append(-2.7)
        times.append(0.6)


# TALK WITH ONLY ONE ARM AND HAND MOVING
def new_talk(robot, n_hands = 2):
    session = robot.service("ALMotion")
    isAbsolute = True
    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand"]
    jointValues = [0.5, -0.46, 0.892, 1.5, 0.98]
    times = [1.0, 1.0, 1.0, 1.0, 1.0]
    times = [time * 0.7 for time in times]

    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [2.7, -0.07, -0.07]
    times = [0.6, 0.6, 0.6]
    for i in range(2):
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    if n_hands == 2:
        jointNames.append("LElbowYaw")
        jointValues.append(-2.7)
        times.append(0.6)


# SENTENCES
def sentences(index):
    sentence = [
        "Hi, I'm PEPPER ART! Pleased to meet you. I have some puzzles about some works of art, do you want to play with me to solve them?",
        "Great! Let's play together. Before starting the game I want to ask you some questions about yourself.",
        "What is your age?",
        "From 1 to 5 how much do you like solving logic problems?",
        "How patient are you when it comes to solving puzzles?",
        "How much do you like art?",
        "According to what you have said I have chosen the easy level jigsaw puzzle for you.",
        "According to what you have said I have chosen the medium level jigsaw puzzle for you.",
        "According to what you have said I have chosen the hard level jigsaw puzzle for you.",
        "You made 3 incorrect moves, can I help you by doing 2 correct moves?",
        "You have completed the jigsaw puzzle, congratulation!",
        "Goodbye, it was a pleasure playing with you."
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

def move_talk(robot, text, char, service):

    if char == "greeting":
        move_greeting(robot)

    if char == "talk":
        talk(robot)

    if char == "new talk":
        new_talk(robot)
        
    if char == "talk1":
        talking1(robot)

    if char == "talk2":
        talking2(robot)

    if char == "talk3":
        talking3(robot)
    
    if char == "no":
        no_with_head(robot)
    
    if char == "goodbye":
        goodbye(robot)
    
    if char == "final dance":
        final_dance(robot)
    
   
    service.say(text)
    return

################## INITIAL MOVES, IT GREET AND ASK YOU IF YOU WANT TO PLAY ##############################
def greeting(session, tts_service):
    sentence = sentences(0)
    move_talk(robot=session, text=sentence, char="greeting", service=tts_service)
##########################################################################################################


################## QUESTIONNARIE ABOUT THE DIFFICULTY TO SUGGEST #########################################
def questionaire(client, session, tts_service):
    introduction_sentence = sentences(1)
    move_talk(robot=session, text=introduction_sentence, char="talk", service=tts_service)

    age_question = sentences(2)
    move_talk(robot=session, text=age_question, char=" ", service=tts_service)
    age = input_thread("Enter your age in number: ", client)
    print(age)

    logic_puzzle_question = sentences(3)
    move_talk(robot=session, text=logic_puzzle_question, char="new talk", service=tts_service)
    attitude_to_logic =input_thread("Enter your answer (1,2,3,4,5): ",client)

    patience = sentences(4)
    move_talk(robot=session, text=patience, char="talk", service=tts_service)
    how_much_patience = input_thread("Enter your answer (little, enough, a lot): ",client)

    art = sentences(5)
    move_talk(robot=session, text=art, char = "", service=tts_service)
    like_art = input_thread("Enter you anser (little, enough, a lot): ",client)


    if age and attitude_to_logic and how_much_patience and like_art:
        if age < 10 and attitude_to_logic <= 4 and how_much_patience.lower() in ["little, enough"] and like_art.lower() in ["little, enough"]:
            difficulty = difficulties(0)
        
        elif age < 10 and attitude_to_logic > 4 and how_much_patience.lower() in ["enough, a lot"] and like_art.lower() in ["enough, a lot"]:
            difficulty = difficulties(1)

        elif 10 <= age <= 18 and attitude_to_logic <= 3 and how_much_patience.lower() in ["little, enough"] and like_art.lower() in ["little"]:
            difficulty = difficulties(0)
        
        elif 10 <= age <= 18 and 3 <= attitude_to_logic <= 4 and how_much_patience.lower() in ["enough, a lot"] and like_art.lower() in ["enough, a lot"]:
            difficulty = difficulties(1)
        
        elif 10 <= age <= 18 and attitude_to_logic == 5 and how_much_patience.lower() in ["a lot"] and like_art.lower() in ["a lot"]:
            difficulty = difficulties(2)
        
        elif age > 18 and attitude_to_logic <= 3 and how_much_patience.lower() in ["little, enough"] and like_art.lower() in ["little, enough"] :
            difficulty = difficulties(1)
        
        elif age > 18 and attitude_to_logic > 3 and how_much_patience.lower() in ["enough, a lot"] and like_art.lower() in ["enough, a lot"]:
            difficulty = difficulties(2)
        else:
            difficulty = difficulties(1)
        return difficulty
    else: 
        return None
##########################################################################################################


############## PEPPER MOVES AND SUGGEST YOU THE DIFFICULTY BASED ON THE QUESTIONNAIRE ####################
def suggest_difficulty(session, tts_service, difficulty):
    difficulty_sentences = {
        "easy": 6,
        "medium": 7,
        "hard": 8
    }
    sentence_index = difficulty_sentences.get(difficulty.lower())
    if sentence_index is not None:
        sentence = sentences(sentence_index)
        move_talk(robot=session, text=sentence, char="new talk", service=tts_service)
##########################################################################################################



############# PEPPER SAYS THAT YOU MADE 3 ERRORS AND MAKES 2 MOVE FOR YOU ################################   
def makes_move_for_you(session, tts_service):
    sentence = sentences(9)
    move_talk(robot=session, text=sentence, char="talk", service=tts_service)
##########################################################################################################



############## PEPPER MAKES THE FINAL DANCE TO CELEBRATE THE VICTORY #####################################    
def final(session, tts_service):
    sentence = sentences(10)
    move_talk(robot=session, text=sentence, char="final dance", service=tts_service)
##########################################################################################################
    


############## PEPPER SAYS GOODBYE AT THE END OF THE GAME ################################################
def goodbye_and_talk(session, tts_service):
    sentence = sentences(11)
    move_talk(robot=session, text=sentence, char="goodbye", service=tts_service)
##########################################################################################################
       


if __name__ == '__main__':
    pip = os.getenv('PEPPER_IP')
    pport = 9559
    url = "tcp://" + pip + ":" + str(pport)
    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session   

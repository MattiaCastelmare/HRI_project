""" 
Implementation of the speech of Pepper and its motion
"""

import qi
import os 
import sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
import pepper_cmd
from pepper_cmd import *

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

# 1st STRANGE TALKING
def talking1(robot):
    session = robot.service("ALMotion")
    isAbsolute = True
    jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
    jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]
    t = 1.0
    times  = [t] * len(jointNames)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    for i in range(2):
        jointNames = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
        jointValues = [1.5, 1.0, -1.2]
        times  = [0.6, 0.6, 0.6]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        jointNames = ["LShoulderPitch", "LElbowRoll", "LWristYaw"]
        jointValues = [1.5, -1.0, 1.2]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    for i in range(2):
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["RShoulderPitch", "RElbowRoll", "RWristYaw"], jointValues, times, isAbsolute)
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["LShoulderPitch", "LElbowRoll", "LWristYaw"], jointValues, times, isAbsolute)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    return

# 2nd STRANGE TALKING
def talking2(robot):
    session = robot.service("ALMotion")
    isAbsolute = True
    jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
    jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]
    t = 1.0
    times  = [t] * len(jointNames)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    for i in range(2):
        jointNames = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
        jointValues = [1.5, 1.0, -1.2]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        jointNames = ["LShoulderPitch", "LElbowRoll", "LWristYaw"]
        jointValues = [1.5, -1.0, 1.2]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["RShoulderPitch", "RElbowRoll", "RWristYaw"], jointValues, times, isAbsolute)
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["LShoulderPitch", "LElbowRoll", "LWristYaw"], jointValues, times, isAbsolute)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    return

# 3rd STRANGE TALKING
def talking3(robot):
    session = robot.service("ALMotion")
    isAbsolute = True
    jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
    jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]
    t = 1.0
    times = [t] * len(jointNames)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    for i in range(2):
        jointNames = ["RShoulderPitch", "LShoulderPitch", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw"]
        jointValues_up = [1.5, 1.5, 1.0, -1.0, -1.2, 1.2]
        session.angleInterpolation(jointNames, jointValues_up, times, isAbsolute)
        jointValues_down = [-0.141, -0.141, 0.892, 0.892, -0.8, -0.8]
        session.angleInterpolation(jointNames, jointValues_down, times, isAbsolute)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    return

# GOODBYE
def goodbye(robot):
    raiseArm(robot, "R")
    waveArm(robot, "R")
    return

# RAISE ARMS
def raiseArms(robot):
    session = robot.service("ALMotion")
    jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
                  "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
    jointValues = [1.5, 0.3, 0.0, 0.2, 0.0, 1.5, -0.3, 1.22, 0.52, -1.08]

    times = [1.0] * len(jointNames)
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

# NORMALE TALK
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

# SENTENCES
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
        "You made 3 incorrect moves, can I help you by doing 2 correct moves?",
        "You have completed the jigsaw puzzle, congratulation!",
        "Goodbye it was a pleasure playing with you"
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
        dance(robot)
    
   
    service.say(text)
    return

def greeting(session, tts_service):
    sentence = sentences(0)
    move_talk(robot=session, text=sentence, char="greeting", service=tts_service)
    answer = raw_input("Enter your answer (yes, no): ")
    return answer

def ask_questions(session, tts_service):
    introduction_sentence = sentences(1)
    move_talk(robot=session, text=introduction_sentence, char="talk", service=tts_service)

    age_question = sentences(2)
    move_talk(robot=session, text=age_question, char=" ", service=tts_service)
    age = raw_input("Enter your age in number: ")

    logic_puzzle_question = sentences(3)
    move_talk(robot=session, text=logic_puzzle_question, char="talk", service=tts_service)
    attitude_to_logic = raw_input("Enter your answer(yes, no, not so much): ")

    if age < 10:
        difficulty = difficulties(0) if attitude_to_logic.lower() in ["no", "not so much"] else difficulties(1)
    elif 10 <= age <= 18:
        difficulty = difficulties(1) if attitude_to_logic.lower() in ["no", "not so much"] else difficulties(2)
    else:
        difficulty = difficulties(1) if attitude_to_logic.lower() in ["no", "not so much"] else difficulties(2)
    return difficulty

def Pepper_moves(session, tts_service):
    sentence = sentences(9)
    move_talk(robot=session, text=sentence, char="talk", service=tts_service)

def suggest_difficulty(session, tts_service, difficulty):
    difficulty_sentences = {
        "easy": 4,
        "medium": 5,
        "hard": 6
    }
    sentence_index = difficulty_sentences.get(difficulty.lower())
    if sentence_index is not None:
        sentence = sentences(sentence_index)
        move_talk(robot=session, text=sentence, char="talk", service=tts_service)

    
def final(session, tts_service):
    sentence = sentences(10)
    move_talk(robot=session, text=sentence, char="final dance", service=tts_service)

def goodbye_and_talk(session, tts_service):
    sentence = sentences(11)
    move_talk(robot=session, text=sentence, char="goodbye", service=tts_service)

def makes_move_for_you(session, tts_service):
    sentence = sentences(9)
    move_talk(robot=session, text=sentence, char="talk", service=tts_service)

if __name__ == '__main__':
    pip = os.getenv('PEPPER_IP')
    pport = 9559
    url = "tcp://" + pip + ":" + str(pport)
    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session   

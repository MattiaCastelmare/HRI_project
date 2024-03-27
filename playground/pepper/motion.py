""" 
Implementation of the speech of Pepper and its motion
"""
import os, sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
from pepper_cmd import *
from utils import *

# Action that moves the head of the robot 
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

# Action that makes the robot saying "no" with its head
def no_with_head(robot):
    look(robot, "left")
    look(robot, "right")
    return

# Action that makes the robot raising its hand above the head
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

# Action that makes the robot raising its hands above the head
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

# Action that makes the robot waving one hand
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

# Action that makes the robot greeting with one hand
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

# Action that makes the robot saying goodbye
def goodbye(robot):
    raiseArm(robot, "R")
    waveArm(robot, "R")
    return
# Action that makes the robot dancing at the end of game
def final_dance(robot):
    session = robot.service("ALMotion")
    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
    jointValues = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07, -0.141, 0.46, -0.892, 0.8, 0.98]
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

# Action that makes the robot normal talking
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

# Action that makes the robot showing the tablet before starting
def show(robot, n_hands=2):
    session = robot.service("ALMotion")
    isAbsolute = True
    jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", 
                  "RElbowYaw", "RHand", "HipRoll", "HeadPitch"]
    jointValues = [1.2, -0.46, 3, 1.5, 1, 0.98, -0.07, 0.7]  # Adjust the value of RElbowYaw according to your requirement
    times = [1.0, 1.0, 1.0, 1.0, 0.6, 1.0, 1.0, 1.0]
    times = [time * 0.7 for time in times]
    
    if n_hands == 2:
        jointNames += ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", 
                       "LElbowYaw", "LHand"]
        jointValues += [1.2, 0.46, -3, -1.5, -1, 0.98]
        times += [0.7 for _ in range(6)]
    for i in range(3):
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

# Action that makes the robot talking with only one hand
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
        
# Action that makes the robot moving and saying something good to the user when it does a good move
def cheering(robot, which='R'): # or 'R'/'L' for right/left arm
    session = robot.service("ALMotion")

    # Store the initial joint values
    if (which=='R'):
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
        initialJointValues = session.getAngles(jointNames, True)

        # Perform the cheering motion
        jointValues = [-0.1, 0.2, 1.57, 1.57, 1.0, -1.0]  # Added RWristYaw and RHand
        times = [1]*len(jointNames)  # Added time for the hand
        isAbsolute = True
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

        # Return to the initial position as fast as possible
        session.angleInterpolation(jointNames, initialJointValues, times, isAbsolute)
    return

# Initalization of the robot
def initialize_robot():
    pip = os.getenv('PEPPER_IP')

    pport = 9559

    url = "tcp://" + pip + ":" + str(pport)

    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session 

    tts_service = session.service("ALAnimatedSpeech")

    return session, tts_service

# Different action combined with the speech
def move_talk(robot, text, char, service):

    if char == "greeting":
        move_greeting(robot)

    if char == "talk":
        talk(robot)

    if char == "new talk":
        new_talk(robot)
        
    if char =="good move":
        cheering(robot)
        
    if char == "bad move":
        talk(robot)
    if char == "no":
        no_with_head(robot)
    
    if char == "goodbye":
        goodbye(robot)
    
    if char == "final dance":
        final_dance(robot)
    if char == "show":
        show(robot)
    
   
    service.say(text)
    return

############################################################################################################################    
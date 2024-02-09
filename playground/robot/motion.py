""" 
In this code it is implemented motion of Pepper and its speech

"""
import qi
import os 
import sys
sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
import pepper_cmd
from pepper_cmd import *

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

def no_with_head(robot):

    look(robot, "left")
    look(robot, "right")

    return

def raiseArm(robot, which='R'): # or 'R'/'L' for right/left arm
    session = robot.service("ALMotion")
    if (which=='R'):
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        # Adjusted joint values to keep the arm raised above the head
        jointValues = [ -1.0, -0.3, 1.22, 0.52, -1.08] 
    else:
        jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        # Adjusted joint values to keep the arm raised above the head
        jointValues = [ 1.5, 0.3, 0.0, 0.2, 0.0] 
    times = [1.0, 1.0, 1.0, 1.0, 1.0]
    isAbsolute = True

    pause = 1 # how much time you want to keep the hand over the head
    for i in range(pause):
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)


    return

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

def greeting(robot):
  # Robot's animation to greet people
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

def talking(robot):
    # Robot's animation to simulate talking
    session = robot.service("ALMotion")
    
    isAbsolute = True

    # Initial position for greeting
    jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
    jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]

    t = 1.0
    times  = [t] * len(jointNames)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    
    # Both arms moving up
    for i in range(2):
        # Right arm up
        jointNames = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
        jointValues = [1.5, 1.0, -1.2]
        times  = [0.6, 0.6, 0.6]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

        # Left arm up
        jointNames = ["LShoulderPitch", "LElbowRoll", "LWristYaw"]
        jointValues = [1.5, -1.0, 1.2]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    # Both arms moving down
    for i in range(2):
        # Right arm down
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["RShoulderPitch", "RElbowRoll", "RWristYaw"], jointValues, times, isAbsolute)

        # Left arm down
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["LShoulderPitch", "LElbowRoll", "LWristYaw"], jointValues, times, isAbsolute)

    # Return to initial position
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    return

def talking2(robot):
    # Robot's animation to simulate talking
    session = robot.service("ALMotion")
    
    isAbsolute = True

    # Initial position for greeting
    jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
    jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]

    t = 1.0
    times  = [t] * len(jointNames)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    
    # Both arms moving up and down
    for i in range(2):
        # Right arm up
        jointNames = ["RShoulderPitch", "RElbowRoll", "RWristYaw"]
        jointValues = [1.5, 1.0, -1.2]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

        # Left arm up
        jointNames = ["LShoulderPitch", "LElbowRoll", "LWristYaw"]
        jointValues = [1.5, -1.0, 1.2]
        session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

        # Right arm down
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["RShoulderPitch", "RElbowRoll", "RWristYaw"], jointValues, times, isAbsolute)

        # Left arm down
        jointValues = [-0.141, 0.892, -0.8]
        session.angleInterpolation(["LShoulderPitch", "LElbowRoll", "LWristYaw"], jointValues, times, isAbsolute)

    # Return to initial position
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    return
def talking3(robot):
    # Robot's animation to simulate talking
    session = robot.service("ALMotion")
    
    isAbsolute = True

    # Initial position for greeting
    jointNames = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw", "RHand", "LHand", "HipRoll", "HeadPitch"]
    jointValues = [-0.141, -0.141, -0.46, 0.46, 0.892, 0.892, -0.8, -0.8, 0.98, 0.98, -0.07, -0.07]

    t = 1.0
    times = [t] * len(jointNames)
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    
    # Both arms moving up and then down
    for i in range(2):
        # Both arms up
        jointNames = ["RShoulderPitch", "LShoulderPitch", "RElbowRoll", "LElbowRoll", "RWristYaw", "LWristYaw"]
        jointValues_up = [1.5, 1.5, 1.0, -1.0, -1.2, 1.2]
        session.angleInterpolation(jointNames, jointValues_up, times, isAbsolute)

        # Both arms down
        jointValues_down = [-0.141, -0.141, 0.892, 0.892, -0.8, -0.8]
        session.angleInterpolation(jointNames, jointValues_down, times, isAbsolute)

    # Return to initial position
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    return



if __name__ == '__main__':
    
    
    pip = os.getenv('PEPPER_IP')

    pport = 9559

    url = "tcp://" + pip + ":" + str(pport)

    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session
    #greeting(session)
    # raiseArm(session, "R")
    # waveArm(session, "R")
    # talking(session)
    # talking2(session)
    talking3(session)




    

    
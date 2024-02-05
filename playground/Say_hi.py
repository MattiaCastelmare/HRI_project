
import os, sys
from naoqi import ALProxy
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
# Import necessary modules
from naoqi import ALProxy
import random
import time

# Set the IP address and port of your Pepper robot
PEPPER_IP = "127.0.0.1"  # Replace with the actual IP address of your Pepper
PEPPER_PORT = 9559

# Connect to the ALMotion module
motion_proxy = ALProxy("ALMotion", PEPPER_IP, PEPPER_PORT)

# Function to move a puzzle piece in a random direction
def move_puzzle_piece():
    # Define the possible directions (for simplicity, assuming 4 directions: forward, backward, left, right)
    directions = ["Forwards", "Backwards", "Left", "Right"]

    # Choose a random direction
    random_direction = random.choice(directions)

    # Set the appropriate motion parameters based on the chosen direction
    if random_direction == "Forwards":
        motion_proxy.moveTo(0.1, 0, 0)
    elif random_direction == "Backwards":
        motion_proxy.moveTo(-0.1, 0, 0)
    elif random_direction == "Left":
        motion_proxy.moveTo(0, 0.1, 0)
    elif random_direction == "Right":
        motion_proxy.moveTo(0, -0.1, 0)

    # Wait for the movement to complete (you can adjust the sleep duration based on your needs)
    time.sleep(2)

# Call the function to move a puzzle piece in a random direction
move_puzzle_piece()



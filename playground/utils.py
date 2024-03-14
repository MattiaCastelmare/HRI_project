# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop, tornado.websocket, tornado.httpserver
import threading, time
from threading import Timer 
import select
import random, re

############################################# SHARED CONSTANTS #####################################################
# Set the Server IP as the local host (of my PC)
IPAddress = "0.0.0.0" # ACCEPT ALL CONNECTIONS 
server_port = "8888"
websocket_address = "ws://"+IPAddress+":"+ server_port + "/websocket"
print("The server has address: " + websocket_address)

# Pepper robot simulation connection 
session = None
tts_service = None

#import socket
# SERVER IP
# Get the external IP address
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("0.0.0.0", 80))  
#IPAddress = s.getsockname()[0]
#IPAddress = "10.0.2.2" # STANDARD FOR ANDROID STUDIO
#print('Your Computer IP Address is: ' + IPAddress)

############################################ PLANNING CONSTANTS ####################################################
algorithm_name= "ehs"
heuristic_name= "landmark"

############################################ TIMED INPUT FUNCTION #################################################
timeout = 10 # global timeout set to 10 seconds
# Function that returns None if no input is received 
def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    else:
        return None

########################################### UTILITY SHOWS ACTIVE THREADS ##########################################
def print_active_threads():
    print("Active threads:", threading.active_count())
    print("Thread IDs:", threading.enumerate())

############################################# PEPPER  SENTENCES ####################################################
def sentences(index):
    sentence = [
        "Hi, I'm PEPPER ART! Pleased to meet you. I have some puzzles about some works of art, do you want to play with me to solve them?",
        "Before starting the game I want to ask you some questions about yourself.",
        "What is your age?",
        "From 1 to 5 how much do you like solving logic problems?",
        "How patient are you when it comes to solving puzzles?",
        "How much do you like art?",
        "According to what you have said I have chosen the EASY level jigsaw puzzle for you.",
        "According to what you have said I have chosen the MEDIUM level jigsaw puzzle for you.",
        "According to what you have said I have chosen the HARD level jigsaw puzzle for you.",
        "You made 3 incorrect moves, can I help you by doing 2 correct moves?",
        "You have completed the puzzle, congratulation!",
        "Goodbye! Come closer again if you decide to play with me!",
        "Great! Let's play together. "
    ]
    return sentence[index]

####################################### RETURN DIFFICULTIES STRING ###############################################
def difficulties(index):
    difficulty = [
            "easy",
            "medium",
            "hard" 
        ]
    return difficulty[index]

######################################## GOOD SENTENCES ############################################
def good_sentences():
    good_sentences = [
        "Great move!",
        "Keep it up!",
        "Well done"
    ]
    return random.choice(good_sentences)

######################################## BAD SENTENCES ############################################
def bad_sentences():
    bad_sentences = [
        "Pay attention!",
        "Ops.. it seems you made an error",
        "Maybe this move is not the best one I am here to help you!"
    ]
    return random.choice(bad_sentences)

########################################### DESCRIPTIONS OF THE PAINTINGS ########################################
paintings_info = {
    'bedroom': {
        'adult': "‘The Bedroom’ is a work by Vincent van Gogh, painted in 1888. It represents his room in Arles, France, with a deliberately distorted perspective. Van Gogh used vibrant colors and bold brushstrokes to capture the essence of his daily life. It’s interesting to note that the distorted perspective and bold use of color reflect his unique and revolutionary approach to art.",
        'children': "This colorful painting is called ‘The Bedroom’. Vincent van Gogh painted it in 1888, a long time ago! It’s his room in Arles, France. Look at how he used bright colors and bold brushstrokes to make it unique! Do you know that he painted three different versions of this same room?"
    },
    'country_field': {
        'adult': "This vibrant painting is ‘Wheat Field with Cypresses’ by Vincent van Gogh, painted in 1889. It depicts a golden wheat field under a swirling sky, with a tall cypress tree standing out. Van Gogh’s expressive brushwork gives a sense of movement and life to the scene.",
        'children': "Look at this painting! It’s called ‘Wheat Field with Cypresses’. It was made by Vincent van Gogh in 1889. See the swirly clouds in the sky? And the tall, pointy tree? They’re all dancing in the wind!"
    },
    'crow': {
        'adult': "This expressive painting is ‘Wheat Field with Crows’ by Vincent van Gogh, painted in 1890. It is often claimed that this was his very last work. The menacing sky, the crows and the dead-end path are said to refer to the end of his life approaching.",
        'children': "This beautiful painting is called ‘Wheat Field with Crows’ by an artist named Vincent van Gogh. He made it way back in 1890. Can you see the black birds flying in the sky? And the wheat field looks like a sea of gold, waving thanks to the wind!"
    },
    'iris': {
        'adult': "This is ‘Irises’ by Vincent van Gogh, painted in 1890 , just before he checked himself out of the asylum at Saint-Rémy. It features a bouquet of vibrant blue irises elegantly placed in a simple white vase. He sought a “harmonious and soft” effect by placing the “violet” flowers against a “pink background,” which have since faded owing to his use of fugitive red pigments.",
        'children': "This is a painting called ‘Irises’.  In art this kind of painting is called still life, however Van Gogh gave is personal touch. That’s why the flowers look so bright and lively! And guess what, he didn’t think this painting was finished, but everyone else loved it just the way it is!"
    },
    'kandinsky': {
        'adult': "This is an abstract work of art made by Wassily Kandinsky, a pioneer of this new twentieth-century art movement. The name of this painting is ‘Yellow, red, blue’ and was painted in 1925. It features a dynamic composition of geometric shapes and lines, mixed with vibrant colors. Kandinsky skillfully balanced both chaotic and harmonious elements, inviting the viewer to deep reflection on the complexity and intrinsic beauty of existence.",
        'children': "This colorful painting was made by a famous artist named Wassily Kandinsky and it is named ‘Yellow, red, blue’. It’s like a puzzle full of shapes like circles and squares in bright colors. Every time you look at it, you can discover something new! It’s a treasure trove of surprises!"
    },
    'napoleon': {
        'adult': "This painting is one of the oil on canvas series Napoleon Crossing the Alps,  equestrian portraits of Napoleon Bonaparte painted by the French artist Jacques-Louis David between 1801 and 1805. The composition shows a strongly idealized view of the real crossing that Napoleon and his army made along the Alps through the Great St Bernard Pass in May 1800.",
        'children': "The man on the horse was Napoleon Bonaparte, a very important historical figure in European history. He commissioned the painting to a French painter and told him to depict him in an heroic pose. It’s like he’s in a superhero pose!"
    },
    'self_portrait': {
        'adult': "In 1886, Vincent van Gogh moved to Paris where his brother Theo worked as an art dealer. During his time there, he painted many self-portraits, including this one. He painted this on a prepared artist's board. His style, characterized by densely dabbed brushwork, was influenced by Georges Seurat's pointillist technique. van Gogh used this as an intense emotional language, seen in the vibrant colors and the piercing gaze of his green eyes. He wrote that he found painting people's eyes more captivating than painting cathedrals because they reveal the depths of the human soul.",
        'children': "Vincent van Gogh was an artist who painted a lot of selfies! He moved to Paris where his brother worked. In Paris, he painted this picture using lots of tiny dots and dashes. His eyes, painted a deep green, stand out and seem to look right at you! Van Gogh said he liked painting people's eyes more than big buildings because eyes show what people feel inside."
    },
    'starry_night': {
        'adult': "Vincent van Gogh painted 'The Starry Night' while staying at an asylum in southern France, where he sought relief from his mental struggles. The vision took place at night, yet the painting was created during the day. The village was not visible from the actual viewpoint, and the cypress tree was not as close as portrayed in the painting. Van Gogh assigned an emotional language to night and nature that took them far from their actual appearances. Dominated by vivid blues and yellows applied with gestural verve and immediacy.",
        'children': "Vincent van Gogh painted this picture called 'The Starry Night', by looking outside his window. Even though he painted during the day, he used his imagination to re-create the beautiful night sky with bright stars and a big yellow moon. He used lots of bright colors and big brushstrokes to make it look magical!"
    },
    'the_wave': {
        'adult': "\"The Great Wave off Kanagawa\" is Hokusai's most famous piece and the first in his series called Thirty-six Views of Mount Fuji. It marked a breakthrough in Japanese prints by introducing Prussian blue. The composition blends traditional Japanese style with European graphical perspective, leading to immediate acclaim in Japan and later in Europe. The print's influence extended to Impressionist artists. Only a few dozen prints are believed to have survived, held in museums worldwide.",
        'children': "\"Did you know that 'The Great Wave off Kanagawa' is like a superstar among paintings? It's the most famous picture by Hokusai, who was a very talented artist from Japan. He painted lots of pictures showing Mount Fuji, and this one is special because it has a big, curly wave and tiny boats! Everybody loved it, even artists in faraway places like Europe. They copied it and made their own versions. Isn't that cool?"
    },
    'women': {
        'adult': "\"The Virgin\" is a painting by Gustav Klimt, created in 1913 and housed in the National Gallery in Prague. The artwork depicts a group of intertwined female bodies, with a central figure (the virgin) adorned in a swirling-patterned dress, extending her arms in a state of ecstasy. This gesture suggests the awakening of her emotions and sexual desires. To Klimt, someone asleep is not responsible for their desires. He therefore depicted an innocent virgin held captive by her sweet and luscious dreams. Unlike Klimt's earlier \"secessionist\" works, this painting features softer brushstrokes and purer colors.",
        'children': "\"Let's talk about a painting called 'La Vergine' by Gustav Klimt. It's like a big puzzle of women all tangled up together! In the middle, there's a beautiful lady wearing a pretty dress with swirls and flowers on it. This painting is full of bright and soft colors. So, why do you she is stretching her arms? What is she dreaming about?"
    }
}

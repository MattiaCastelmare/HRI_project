
# -*- coding: utf-8 -*-
import tornado.ioloop
import random
import re
#import tornado.web
import tornado.websocket
import socket
import os
#import tornado.gen
import threading, time
from threading import Timer 
import sys
import select


# SERVER IP
# Get the external IP address
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("0.0.0.0", 80))  
#IPAddress = s.getsockname()[0]
#IPAddress = "10.0.2.2" # STANDARD FOR ANDROID STUDIO
IPAddress = "0.0.0.0" # CONNECT TO ALL PORTS
print('Your Computer IP Address is: ' + IPAddress)

# Set the Server IP as the local host (of my PC)
server_port = "8888"
#print("Websocket server for Pepper listening on port: " +  server_port)
websocket_address = "ws://"+IPAddress+":"+server_port + "/websocket"
print("The server has this address: " + websocket_address)

# PLANNING CONSTANTS
algorithm_name= "ehs"
heuristic_name= "landmark"


class MyTimer:
    def __init__(self, timeout_duration):
        self.timeout_duration = timeout_duration
        self.timer = None 
        print("Timers have been set to wait for " + str(self.timeout_duration) +" seconds")

    def timeout_handler(self):
        print("\nTIME OVER!")
        # CHE FA PEPPER ?

    def start(self): 
        self.timer = Timer(self.timeout_duration, self.timeout_handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()
        self.timer = None 


def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()

    ready, _, _ = select.select([sys.stdin], [], [], timeout)

    if ready:
        return sys.stdin.readline().strip()
    else:
        return None


user_input = None
input_lock = threading.Lock()
stop_flag=True

def my_input(text, client):
    global user_input, stop_flag
    local_input = None
    stop_flag=True
    while stop_flag:
        time.sleep(1)
        if client.stop_questions:
            break
        local_input = input_with_timeout("INPUT in another thread: " + text,10)
        if local_input:
            with input_lock:
                user_input = local_input
            break

    return

def input_thread(text, client):
    global user_input,stop_flag
    thread = threading.Thread(target=my_input, args=(text,client))
    #thread.daemon = True
    thread.start()
    thread.setName('questionThread')
    thread.join(timeout=10)

    if thread.is_alive():
       stop_flag=False
       #thread._Thread__stop()  
       return user_input, True
    else:
        return user_input, False
    

#prova per vedere numeri thread
def print_active_threads():
    print("Active threads:", threading.active_count())
    print("Thread IDs:", threading.enumerate())


## DESCRIPTIONS OF PTHE PAINTINGS
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
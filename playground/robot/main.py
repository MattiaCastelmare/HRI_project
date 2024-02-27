import qi
import os
import sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*
from client import*

sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
import pepper_cmd
from pepper_cmd import*
from motion import*

puzzle_completed = True
sequence_incorrect = True

def try_connection(session, tts_service):
    io_loop = tornado.ioloop.IOLoop.current()
    client = PepperClient(io_loop=io_loop, session=session, tts_service=tts_service)
    io_loop.add_callback(client.start)
    io_loop.start()

def main():
    session, tts_service = initialize_robot()
    answer = greeting(session=session, tts_service=tts_service)
    if answer.lower() == "yes":
        try_connection(session, tts_service)
        #difficulty = ask_questions(session=session, tts_service=tts_service)
        suggest_difficulty(session=session, tts_service=tts_service, difficulty=difficulty)
        if sequence_incorrect:
            Pepper_moves(session=session, tts_service=tts_service)

        if puzzle_completed:
            final(session=session, tts_service=tts_service)
   
    goodbye_and_talk(session=session, tts_service=tts_service)
    return  

if __name__ == "__main__":
    main()
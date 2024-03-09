import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(user_dir)
from utils import*
from pddl_planning.solver import Planning

# HANDLES THE MAIN HTTP REQUEST FOR THE WEBSOCKET SERVER
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("WebSocket Server is running.")

########################################## WEBSOCKET SERVER ################################################################
class Server(tornado.websocket.WebSocketHandler):
    clients = []  # Connected clients
    puzzleSolver = None  # Pddl Solver
    moves = []  # Store Pepper's moves
   
    # WHEN CONNECTION IS OPENED WITH A CLIENT
    def open(self):
        # Extract client name from the URL
        client_name = self.get_client_name_from_uri(self.request.uri)
        print("WebSocket opened for " + client_name)
        client_dict = {'name': client_name, 'info': self}
        Server.clients.append(client_dict)
        
    # HANDLE INCOMING WEBSOCKET MESSAGES
    def on_message(self, message):
        client_name = self.get_client_name_from_uri(self.request.uri)
        print("Received message from " + client_name + ": " + message)

        if message == ("Go back waiting"):
            Server.forward_message(self, message)

        if message == ("User wants to play"):
            Server.forward_message(self, message)
        
        if message == "Button pressed":
            Server.forward_message(self, message)
        
        if message.startswith("The suggested difficulty"):
            Server.forward_message(self, message)

        if message.startswith("Painting name:"):
            Server.forward_message(self, message)
        
        if message == "Play again":
            Server.forward_message(self,message)

        if message == "Win":
            Server.forward_message(self,message)
            
        if message == "Game started":
            Server.forward_message(self,message)
            
        if message == "Exit":
            Server.forward_message(self,message)

        if message.startswith("Initial random indices:"):
            # Initialize Planning
            Server.puzzleSolver = Planning(algorithm_name=algorithm_name, heuristic_name=heuristic_name)
            # Divide the string in two parts
            index_part = message.split(": ")[1].strip("[]")
            # Put the indices in a list
            first_indices = [int(elem.strip()) for elem in index_part.split(",")]
            swaps, play_well = Server.puzzleSolver.solve(first_indices)

        if  message.startswith("New indices:"):
            index_part = message.split(": ")[1].strip("[]")
            index_list = [int(elem.strip()) for elem in index_part.split(",")]
            swaps, play_well = Server.puzzleSolver.solve(index_list)
            if swaps:
                if len(swaps) == 2:
                    Server.moves =swaps
                    Server.forward_message(self, "User made 3 errors")
                elif len(swaps) > 2 or len(swaps)<1:
                    raise Exception("Too many or too little actions")
                else:
                    if not play_well:
                        Server.forward_message(self, "Uncorrect move")
                    else:
                        Server.forward_message(self, "Correct")
                    swap = swaps[0]
                    pos1, pos2 = swap[0], swap[1]
                    mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                    Server.send_message(self, mess_toSend)
            else:
                print("Game Finished")
                Server.forward_message(self, "Game Finished ")

        if message.startswith("Answer is: "):
            if message.endswith("yes"):
                Server.puzzleSolver.oldPlan_len -= 1  

                swap = Server.moves[0]
                pos1, pos2 = swap[0], swap[1]
                mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                Server.forward_message(self, mess_toSend) 

                swap = Server.moves[1]
                pos1, pos2 = swap[0], swap[1]
                mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                Server.forward_message(self, mess_toSend)
        
            if message.endswith("no"): 
                swap = Server.moves[0]
                pos1, pos2 = swap[0], swap[1]
                mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                Server.forward_message(self, mess_toSend) 

    # WHEN CONNECTION WITH A CLIENT IS CLOSED
    def on_close(self):
        print("WebSocket closed")
        # Remove the closed WebSocket from the clients list
        Server.clients = [client_dict for client_dict in Server.clients if client_dict['info'] != self]
    
    # FORWARD THE MESSAGE TO ALL OTHER CONNECTED CLIENTS EXCEPT THE SENDER
    @classmethod
    def forward_message(cls, sender_client, message: str):
        # Forward the message to all other connected clients except the sender
        for client_dict in cls.clients:
            other_client = client_dict['info']
            if other_client != sender_client:
                try:
                    other_client.write_message(message)
                    print("Forwarding " + message + " to " + client_dict['name'])
                except tornado.websocket.WebSocketClosedError:
                    print(f"Client {client_dict['name']} not connected. Not forwarding the message.")
    
    # SEND MESSAGE TO THE SPECIFIED CLIENT
    @classmethod
    def send_message(cls, client, message: str):
        # Send message to the specified client
        for client_dict in cls.clients:
            if client_dict['info'] == client:
                print(f"Sending message {message} to client {client_dict['name']}.")
                client.write_message(message)
                break  # No need to continue searching once the client is found
        else:
            print(f"Client {client_dict['name']} not found.")

    @staticmethod
    def get_client_name_from_uri(uri):
        # Extract client name from the URL
        match = re.match(r'/websocket/(\w+)', uri)
        if match:
            return match.group(1)
        return None
########################################################################################################
    
# CREATE A TORNADO WEB APPLICATION WITH WEBSOCKET SUPPORT.
def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/websocket/Tablet', Server),
        (r'/websocket/Pepper', Server)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )

# RUN THE IO_LOOP OF THE WEBSOCKET APP
def main():
    app = make_app()
    app.listen(server_port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Keyboard Interrupt ...")
        tornado.ioloop.IOLoop.current().stop()

if __name__ == "__main__":
    main()




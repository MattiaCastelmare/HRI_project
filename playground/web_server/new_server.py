import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(user_dir)
sys.path.append(user_dir)
from utils import*
from pddl_planning.solver import Planning
import json
moves=[]
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("WebSocket Server is running.")

class Server(tornado.websocket.WebSocketHandler):
    clients = []
    puzzleSolver = Planning(algorithm_name=algorithm_name, heuristic_name=heuristic_name)
   

    def open(self):
        # Extract client name from the URL
        client_name = self.get_client_name_from_uri(self.request.uri)
        print("WebSocket opened for " + client_name)
        client_dict = {'name': client_name, 'info': self}
        Server.clients.append(client_dict)
        
    def on_message(self, message):
        client_name = self.get_client_name_from_uri(self.request.uri)

        print("Received message from " + client_name + ": " + message)
        if message == "Hello from Pepper Robot!":
            mess = "User wants to play"
            Server.send_message(self, mess)
            Server.forward_message(self, mess)

        if message.startswith("Initial random indices:"):
            # Divide the string in two parts
            index_part = message.split(": ")[1].strip("[]")
            # Put the indices in a list
            first_indices = [int(elem.strip()) for elem in index_part.split(",")]
            swaps = self.puzzleSolver.solve(first_indices)

        if  message.startswith("New indices:"):
            index_part = message.split(": ")[1].strip("[]")
            index_list = [int(elem.strip()) for elem in index_part.split(",")]
            swaps = self.puzzleSolver.solve(index_list)
            if len(swaps) == 2:
                global moves
                moves =swaps
                
                self.forward_message(self, "User made 3 errors")
                # swap = swaps[1]
                # pos1, pos2 = swap[0], swap[1]
                # mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                # Server.send_message(self,mess_toSend)
            elif len(swaps) > 2 or len(swaps)<1:
                raise Exception("Too many or too little actions")
            else:
                swap = swaps[0]
                pos1, pos2 = swap[0], swap[1]
                mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                Server.send_message(self, mess_toSend) 

        
        if message.startswith("Answer is: "):
            if message.endswith("yes"):   
                
                swap = moves[0]
                pos1, pos2 = swap[0], swap[1]
                mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                Server.forward_message(self, mess_toSend) 

                swap = moves[1]
                pos1, pos2 = swap[0], swap[1]
                mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                Server.forward_message(self, mess_toSend)
        
            if message.endswith("no"): 
                swap = moves[0]
                pos1, pos2 = swap[0], swap[1]
                mess_toSend =  "PepperMove:" + str(pos1) + ',' + str(pos2)
                Server.forward_message(self, mess_toSend) 

        # if message == "Game started !":
        #     Server.forward_message(self, message)


    def on_close(self):
        print("WebSocket closed")
        # Remove the closed WebSocket from the clients list
        Server.clients = [client_dict for client_dict in Server.clients if client_dict['info'] != self]
    
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

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/websocket/Tablet', Server),
        (r'/websocket/Pepper', Server)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )

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




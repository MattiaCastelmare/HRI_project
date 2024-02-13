import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(user_dir)
sys.path.append(user_dir)
from utils import*

from run_planning import run_planning, generate_pddl_file

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("WebSocket Server is running.")

class Server(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        # Extract client name from the URL
        client_name = self.get_client_name_from_uri(self.request.uri)
        print("WebSocket opened for " + client_name)
        client_dict = {'name': client_name, 'info': self}
        Server.clients.append(client_dict)
        

    def on_message(self, message):
    # Forward the message to all other connected clients except the sender
        for client_dict in Server.clients:
            other_client = client_dict['info']
            if other_client != self:
                try:
                    other_client.write_message(message)
                    print("Forwarding " + message + " to " + client_dict['name'])
                # QUI NON ENTRA MAI CONTROLLARE 
                except tornado.websocket.WebSocketClosedError:
                    # Handle the case where the WebSocket is closed for the other client
                    print(f"Client {client_dict['name']} not connected. Not forwarding the message.")
        
        
    def on_close(self):
        print("WebSocket closed")
        # Remove the closed WebSocket from the clients list
        Server.clients = [client_dict for client_dict in Server.clients if client_dict['info'] != self]
    
    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message {message} to {len(cls.clients)} client(s).")
        for client_dict in cls.clients:
            client = client_dict['info']
            client.write_message(message)

    @staticmethod
    def get_client_name_from_uri(uri):
        # Extract client name from the URL
        match = re.match(r'/websocket/(\w+)', uri)
        if match:
            return match.group(1)
        return None
    
    
class TabletServer(tornado.websocket.WebSocketHandler):
    client = {}
    
    # Thing useful for the planning
    domain_file = 'puzzle_domain.pddl'
    problem_file = 'puzzle_problem.pddl'
    algorithm= "ehs"
    heuristic= "hff"

    def check_origin(self, origin):
        return True

    def open(self):
        # Extract client name from the URL
        #client_name = self.get_client_name_from_uri(self.request.uri)
        print("WebSocket opened for Tablet client")
        TabletServer.client= {'name': 'Tablet', 'info': self}
        

    def on_message(self, message: str):
    # Forward the message to all other connected clients except the sender
        if message.startswith("New indices:"):
            # Divide the string in two parts
            index_part = message.split(": ")[1].strip("[]")
            # Put the indices in a list
            index_list = [int(elem.strip()) for elem in index_part.split(",")]
            
            # Generate the new pddl files and execute the new pddl
            generate_pddl_file(index_list)
            plan= run_planning(self.domain_file, self.problem_file, self.algorithm, self.heuristic)
            print("The plan is: ", plan)
            
            # Check if plan is empty
            if len(plan) == 0:
                error_message = "No plan available. Unable to perform action."
                self.send_error(error_message)
                return  # Exit the function if there is no plan
            else:
                # Compute the action 
                action=str(plan[0]).split('\n')[0]
                #print("The action chosen is", action)
                
                # Extract the two position to switch
                matches = re.findall(r"p(\d+)", action)

                if len(matches) >= 2:
                    puzzlePos1 = matches[0]
                    puzzlePos2 = matches[1]
                
                #Define the message to send to the web app
                mess_toSend= 'PepperMove:' + str(puzzlePos1)+ ',' + str(puzzlePos2)
                print(mess_toSend)
                self.send_message(mess_toSend)
                return
        
    def on_close(self):
        print("WebSocket closed")
        # Remove the closed WebSocket from the clients list
        TabletServer.client = {}
    
    @classmethod
    def send_message(self, message: str):
        print(f"Sending message {message} to Tablet client")
        client = self.client['info']
        client.write_message(message)
    


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/websocket/Tablet', TabletServer),
        (r'/websocket/Pepper', Server)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )

def main():
    app = make_app()
    app.listen(server_port)
    try:
        tornado.ioloop.PeriodicCallback(lambda: Server.send_message("Periodic message"), 3000).start()
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Keyboard Interrupt ...")
        tornado.ioloop.IOLoop.current().stop()


if __name__ == "__main__":
    main()

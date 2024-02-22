import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(user_dir)
sys.path.append(user_dir)
from utils import*
from run_planning import run_planning, generate_pddl_file

pepperServer = None 
tabletServer = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("WebSocket Server is running.")

class PepperServer(tornado.websocket.WebSocketHandler):
    client_dict={}
    
    def open(self):
        global pepperServer
        pepperServer = self
        # Extract client name from the URL
        client_name = get_client_name_from_uri(self.request.uri)
        print("WebSocket opened for " + client_name)
        self.client_dict = {'name': client_name, 'info': self}
        

    def on_message(self, message):
         print("Received message from " + self.client_dict["name"] + ": " + message)
         try:
            if message.startswith("Difficulty:"):
                print("Forwarding " + message + " to Tablet")
                tabletServer.send_message(message)
                
         except tornado.websocket.WebSocketClosedError:
                # Handle the case where the WebSocket is closed for the other client
                print(f"Client {self.client_dict['name']} not connected. Not forwarding the message.")
        
        
    def on_close(self):
        print("WebSocket closed")
        # Remove the closed WebSocket from the clients list
        self.client_dict = {}
        global pepperServer
        pepperServer = None

    
    def send_message(self, message: str):
        print(f"Sending message {message} to Pepper client")
        client = self.client_dict['info']
        client.write_message(message)
    
    
class TabletServer(tornado.websocket.WebSocketHandler):
    client_dict = {}
    # Thing useful for the planning
    domain_file = 'puzzle_domain.pddl'
    problem_file = 'puzzle_problem.pddl'
    algorithm= "ehs"
    heuristic= "hff"
    oldPlan_len=100000 # Define the number of action of the old planning
    num_error=0 #Define number of errors committed by the user

    def open(self):
        global tabletServer
        tabletServer = self
        # Extract client name from the URL
        client_name = get_client_name_from_uri(self.request.uri)
        print("WebSocket opened for Tablet client")
        self.client_dict= {'name': client_name, 'info': self}
        print(self.client_dict)

    def on_message(self, message: str):
        print("Received message from " + self.client_dict["name"] + ": " + message)
        if message.startswith("New indices:"):
            # Divide the string in two parts
            index_part = message.split(": ")[1].strip("[]")
            # Put the indices in a list
            index_list = [int(elem.strip()) for elem in index_part.split(",")]
            # Generate the new pddl files and execute the new pddl
            generate_pddl_file(index_list)
            plan= run_planning(self.domain_file, self.problem_file, self.algorithm, self.heuristic)
            print("The plan is: ", plan)
            print("the client dict is:", self.client_dict)
            # Check if plan is empty
            if len(plan) == 0:
                self.oldPlan_len=100000
                self.num_error=0
                error_message = "No plan available. Unable to perform action."
                self.send_error(error_message)
                return  # Exit the function if there is no plan
            
            else:       
                # Compute the number of action need to resolve the puzzle
                num_action= len(plan)
                # Select the first action of the plan
                action=str(plan[0]).split('\n')[0]
                #print("The action chosen is", action)
                # Extract the two position to switch
                matches = re.findall(r"p(\d+)", action)
                if len(matches) >= 2:
                    puzzlePos1 = matches[0]
                    puzzlePos2 = matches[1]
                #Define the message to send to the web app
                mess_toSend= 'PepperMove:' + str(puzzlePos1)+ ',' + str(puzzlePos2)
                if num_action >= self.oldPlan_len :
                    self.num_error+=1
                    print(f"The number of user's error are: {self.num_error}")
                if self.num_error==3 and len(plan)>1:
                    # Select the second action of the plan
                    action2=str(plan[1]).split('\n')[0]
                    # Extract the two position to switch
                    matches2 = re.findall(r"p(\d+)", action2)
                    if len(matches2) >= 2:
                        puzzleMove2Pos1 = matches2[0]
                        puzzleMove2Pos2 = matches2[1]
                    mess_toSend = mess_toSend.replace('PepperMove', '2_PepperMove')
                    mess_toSend += ';' + str(puzzleMove2Pos1) + ',' + str(puzzleMove2Pos2)   
                
                self.send_message(mess_toSend)
                self.oldPlan_len= num_action

        if message == "Game Started !":
                print("entra")
                pepperServer.send_message("Game Started")
        return 
            
        
    def on_close(self):
        print("WebSocket closed")
        # Remove the closed WebSocket from the clients list
        self.client_dict = {}
        global tabletServer
        tabletServer = None
    
    def send_message(self, message: str):
        print(f"Sending message {message} to Tablet client")
        print(self.client_dict)
        client = self.client_dict['info']
        client.write_message(message)
    

def get_client_name_from_uri(uri):
    # Extract client name from the URL
    match = re.match(r'/websocket/(\w+)', uri)
    if match:
        return match.group(1)
    return None

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/websocket/Tablet', TabletServer),
        (r'/websocket/Pepper', PepperServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )

def main():
    app = make_app()
    app.listen(server_port)
    try:
        #tornado.ioloop.PeriodicCallback(lambda: Server.send_message("Periodic message"), 3000).start()
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Keyboard Interrupt ...")
        tornado.ioloop.IOLoop.current().stop()


if __name__ == "__main__":
    main()
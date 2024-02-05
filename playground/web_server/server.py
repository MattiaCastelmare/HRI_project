import sys
sys.path.append('/home/robot/playground')
from utils import*

server_port = 8888

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("WebSocket Server is running.")

class ServerPepperSide(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        print("WebSocket opened")
        ServerPepperSide.clients.add(self)

    def on_message(self, message):
        print("Received message : "+ message)

    def on_close(self):
        print("WebSocket closed")
        ServerPepperSide.clients.remove(self)

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/websocket', ServerPepperSide),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(server_port)

    # Get the external IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # Google's public DNS server
    IPAddress = s.getsockname()[0]
    print('Your Computer IP Address is: ' + IPAddress)

    # Debugging print statements
    print("Websocket server for Pepper listening on port %d" % server_port)

    # Start the IOLoop
    tornado.ioloop.IOLoop.current().start()

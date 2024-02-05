import os, sys
user_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(user_dir)
sys.path.append(user_dir)
from utils import*

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("WebSocket Server is running.")

class ServerPepperSide(tornado.websocket.WebSocketHandler):
    clients = set()

    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")
        ServerPepperSide.clients.add(self)

    def on_message(self, message):
        print("Received from Client : "+ message)

    def on_close(self):
        print("WebSocket closed")
        ServerPepperSide.clients.remove(self)
    
    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message {message} to {len(cls.clients)} client(s).")
        for client in cls.clients:
            client.write_message(message)

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/websocket', ServerPepperSide)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )

def main():
    app = make_app()
    app.listen(server_port)
    try:
        tornado.ioloop.PeriodicCallback(lambda: ServerPepperSide.send_message("Periodic message"), 3000).start()
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Keyboard Interrupt ...")
        tornado.ioloop.IOLoop.current().stop()


if __name__ == "__main__":
    main()

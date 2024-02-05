import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import os
import sys
import tornado.gen
import tornado.ioloop
import tornado.websocket
from tornado.httpclient import HTTPRequest

sys.path.append(os.getenv('PEPPER_TOOLS_HOME') + '/cmd_server')
server_port = 8888

python_path = os.getenv('PYTHONPATH')
if python_path:
    sys.path.extend(python_path.split(':'))

import pepper_cmd
from pepper_cmd import *

# SERVER IP (LOCAL HOST of MY PC )
websocket_address = "ws://10.90.109.71:8888/websocket"
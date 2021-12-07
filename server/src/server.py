from sys import path
if '' not in path:
    path.append('')

import socket, threading, ssl
import os
from common.message_type import MessageType
from common.user import User
from message import Message

class Server(object):
    def __init__(self, ip, port) -> None:
        super().__init__()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile=r"F:\Repositories\testServer\server\src\cert.pem")
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')
        self.sock_address = self.sock.getsockname()
        self.is_running = True
        self.active_users = {}
        self.lock = threading.Lock()
    
    def run(self):
        self.sock.listen(50)
        
        while self.is_running:
            try:
                conn, addr = self.sock.accept()
                wrap = self.context.wrap_socket(conn, server_side=True)
                threading.Thread(target=self.message_handler, args=(wrap, addr,)).start()
            except socket.error as err:
                print(err)
                break

    def message_handler(self, conn, addr):
        user = User(conn, addr)
        msg = Message('UTF-8')
        data = msg.receive(conn)
        if len(data) > 1:
            type = msg.identify_message_type(data[0])
            if type is MessageType.JOIN:
                self.active_users[data[1]] = addr
                msg.send(MessageType.SPOX.name, conn)
            else:
                msg.send(MessageType.DENY.name, conn)

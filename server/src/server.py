from sys import path
from typing import Dict
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
        self.context.load_cert_chain(certfile="cert.pem")
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')
        self.sock_address = self.sock.getsockname()
        self.is_running = True
        self.active_users: Dict[str, User] = {}
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
        running = True
        while running:
            user = User(conn, addr)
            username = ''
            msg = Message('UTF-8')
            data = msg.receive(conn)
            if len(data) > 1:
                type = msg.identify_message_type(data[0])
                if type is MessageType.JOIN:
                    username = data[1]
                    self.active_users[username] = user
                    msg.send(MessageType.SPOX.name, conn)
                elif type is MessageType.LIST:
                    list_content = MessageType.LIST.name
                    for name in self.active_users.keys:
                        list_content = list_content + ':' + name
                    msg.send(list_content, conn)
                elif type is MessageType.GIVE:
                    username_to_map = data[1]
                    if username_to_map in self.active_users.keys:
                        ip_addr = self.active_users[username_to_map].get_ip_address()
                        message_content = MessageType.GIVE.name + ':' + username_to_map + ':' + ip_addr
                        msg.send(message_content, conn)
                    else:
                        msg.send(MessageType.DENY.name, conn)
                elif type is MessageType.QUIT:
                    if (username is not '') and (username in self.active_users.keys):
                        self.active_users.pop(username)
                        running = False
                else:
                    msg.send(MessageType.DENY.name, conn)

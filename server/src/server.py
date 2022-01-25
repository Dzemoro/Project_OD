from sys import path
from typing import Dict
if '' not in path:
    path.append('')

import socket, threading, ssl
import os
from common.message_type import MessageType
from common.user import User
from common.message import Message


class Server(object):
    def __init__(self, ip, port) -> None:
        super().__init__()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile=r"./server/src/cert.pem")
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')
        self.sock_address = self.sock.getsockname()
        self.is_running = True
        self.active_users: Dict[str, User] = {}
        self.lock = threading.Lock()
    
    def run(self):
        print("---SERVER IS RUNNING---\n\n")
        self.sock.listen(50)
        
        while self.is_running:
            try:
                conn, addr = self.sock.accept()
                wrap = self.context.wrap_socket(conn, server_side=True)
                threading.Thread(target=self.message_handler, args=(wrap, addr,)).start()
            except socket.error as err:
                print(err)
                self.is_running = False
                break

    def message_handler(self, conn : socket, addr):
        try:
            running = True
            username = ''
            while running:
                user = User(conn, addr, False)
                msg = Message('UTF-8')
                data = msg.receive(conn)
                if len(data) >= 1:
                    type = msg.identify_message_type(data[0])
                    if type is MessageType.JOIN:
                        username = data[1]
                        self.active_users[username] = user
                        msg.send(MessageType.SPOX.name, conn)
                        print(f"{username} has joined to the server!\n")

                    elif type is MessageType.LIST:
                        list_content = MessageType.LIST.name
                        for name in self.active_users.keys():
                            if (name != username) and not self.active_users[name].calling:
                                list_content = list_content + ':' + name
                        msg.send(list_content, conn)

                    elif type is MessageType.MESS:
                        target_username = data[1]
                        target_user = self.active_users[target_username] 
                        message = data[0] + ":" + username + ":" + data[2] + ":" + data[3]
                        msg.send(message, target_user.conn)
                        print("-----------------------------------------------------------\n")
                        print(f"MESSAGE CONTENT: {data[2]}\n")
                        print(f"MESSAGE FROM: {username}\n")
                        print(f"MESSAGE TO: {target_username}\n")
                        print(f"ENCRYPT TYPE: {data[3]}\n")
                        print("-----------------------------------------------------------\n")                        

                    elif type is MessageType.KEYS:
                        target_username = data[1]
                        target_user = self.active_users[target_username] 
                        message = data[0] + ":" + username + ":" + data[2] + ":" + data[3] + ":" + data[4] + ":" + data[5]
                        msg.send(message, target_user.conn)                         

                    elif type is MessageType.KEYR:
                        target_username = data[1]
                        target_user = self.active_users[target_username] 
                        message = data[0] + ":" + username + ":" + data[2] + ":" + data[3] + ":" + data[4] + ":" + data[5]
                        msg.send(message, target_user.conn)                       

                    elif type is MessageType.CONN:
                        self.active_users[username].calling = True 
                        target_username = data[1]
                        target_user = self.active_users[target_username] 
                        message = data[0] + ":" + username
                        msg.send(message, target_user.conn)    

                    elif type is MessageType.CALL:
                        self.active_users[username].calling = True 
                        target_username = data[1]
                        target_user = self.active_users[target_username] 
                        message = data[0] + ":" + username
                        msg.send(message, target_user.conn)

                    elif type is MessageType.LEAV:
                        self.active_users[username].calling = False
                        target_username = data[1]
                        target_user = self.active_users[target_username] 
                        message = data[0] + ":" + username
                        msg.send(message, target_user.conn)

                    elif type is MessageType.LEAR:
                        self.active_users[username].calling = False
                        if data[1] != "":
                            target_username = data[1]
                            target_user = self.active_users[target_username] 
                            message = data[0] + ":" + username
                            msg.send(message, target_user.conn)    

                    elif type is MessageType.QUIT:
                        if (username != '') and (username in self.active_users.keys()):
                            self.active_users.pop(username)
                            msg.send(MessageType.SPOX.name, conn)
                            print(f"{username} has left the server\n")
                            conn.close()
                            running = False
                    else:
                        msg.send(MessageType.DENY.name, conn)
        except socket.error as err:
            if username in self.active_users.keys():
                print(f"{username} has left the server\n")
                self.active_users.pop(username)

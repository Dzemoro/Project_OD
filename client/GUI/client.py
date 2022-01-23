import socket
import ssl
import threading
import sys
import time
from loginGui import *

from phonebookGui import *

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile="C:\\Users\\mciec\\Desktop\\Studia\\OD\\Project_OD\\client\\GUI\\cert.pem") #TODO cert??
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')
        self.conn = self.context.wrap_socket(self.client, server_hostname=str(self.ip))
        self.conn.connect((str(ip), int(port)))
        #self.client.connect((ip, port))

        self.clientHost = ClientHost() #another client
        threading.Thread(target=self.clientHost.start).start()
        time.sleep(2)



    def receive(self):
        while True:
            data = self.conn.recv(1024)
            if data != b'':
                print(self.ip + " === " +  data.decode())
                c = data.decode()

                message_params = c.split(":")


                # Recieved from server data about incoming connection or sth but not sure if this is the right way and should be here or in the clientHost
                # No clue
                if message_params[0] == 'GIVE': 

                    friends_name = message_params[1]
                    friends_ip = message_params[2]
                    friends_port = message_params[3]

                    print("Client wanted to connect switch current connection " + friends_port)
                    self.client.close()
                    #IP WAS RECIVED FROM SERVER NOT GET FROM HERE AND SHOULD BE PARAMETER TOO
                    self.clientToClient(friends_ip, friends_port)
                    self.client.send(("CLIENT TO CLIENT CONNECTION HERE").encode())
                if message_params[0] == 'SPOX': 
                    print("SPOX")
                if message_params[0] == 'LIST': 
                    print("LIST")

    
    def clientToClient(self, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile="C:\\Users\\mciec\\Desktop\\Studia\\OD\\Project_OD\\client\\GUI\\cert.pem") #TODO cert??
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')
        self.conn = self.context.wrap_socket(self.client, server_hostname=str(self.ip))
        self.conn.connect((str(self.ip), int(port)))
        #self.client.connect((self.ip, port))

class Server:
    def __init__(self) -> None:
        self.connections = []
        self.running = True
        pass

    def start(self) -> None:
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('127.0.0.1', 60000))
        self.server.listen(5)
        while self.running:
            conn, addr = self.server.accept()
            print('Connected by', addr)
            self.connections.append(conn)
            threading.Thread(target=self.handle, args=(conn,)).start()

    def handle(self, conn):
        while True:
            data = conn.recv(1024)

            if data != b'':
                print(data.decode())
                if data.decode() == 'QUIT':
                    conn.send(b'Goodbye')
                    conn.close()
                    break
        
    def stop(self):
        self.running = False
        self.server.close()

class ClientHost:
    def __init__(self) -> None:
        self.running = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('',0))
        self.server.listen(5)

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile="C:\\Users\\mciec\\Desktop\\Studia\\OD\\Project_OD\\client\\GUI\\cert.pem") #TODO cert??
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')
        self.sock_address = self.server.getsockname()

    def start(self) -> None:
        # start server
        while self.running:
            conn, addr = self.server.accept()
            print('Connected by on Client Server', addr)
            threading.Thread(target=self.handle, args=(conn,)).start()


    def handle(self, conn):
        while True:
            data = conn.recv(1024)

            if data != b'':
                print(data.decode()) ##handle message
                if data.decode() == 'QUIT':
                    conn.send(b'Goodbye')
                    conn.close()
                    break
    
    def stop(self):
        self.running = False
        self.server.close()

from os import error
import socket
import select
import sys
from threading import Thread
import time
from contextlib import closing
import platform

class Client:
    def __init__(self):
        self.tcp_conn_status = False
        self.server_tcp_port = None
        self.server_address = '127.0.0.1'
        self.nick = 'Anonymous'

        self.guiMessage = 0

        self.BUFF_SIZE = 65536

    def sockets_setup(self):
        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_s.settimeout(1)

    def set_nick(self, nick):
        self.nick = nick

    def set_server_addr(self, ip):
        self.server_address = ip

    def set_server_tcp_port(self, port):
        self.server_tcp_port = port

    def tcpConnection(self):
        data = 'JOIN ' + self.nick
        self.tcp_s.send(bytes(data, 'UTF-8'))
        data = self.tcp_s.recv(1024)
        decoded = data.decode('UTF-8')
        message = decoded.split()
        if (message[0] == "OK"):
            self.tcp_conn_status = True
        else:
            self.tcp_s.shutdown(socket.SHUT_RDWR)
            self.tcp_s.close()

        while(self.tcp_conn_status == True):
            #check if everything is ok
            try:
                ready_to_read, ready_to_write, in_error = \
                    select.select([self.tcp_s,], [self.tcp_s,], [], 5)
            
                if len(ready_to_read) > 0:
                    recv = self.tcp_s.recv(1024)
                    decoded = recv.decode('UTF-8')
                    message = decoded.split()
                    if (message[0] == "LIST"):
                        users = []
                        for i in range(1, len(message)):
                            users.append(message[i])
                        self.usersList = users

                if len(ready_to_write) > 0:
                    self.tcp_s.send(bytes('AWLI', 'UTF-8'))

                time.sleep(1)

            except:
                if(self.tcp_conn_status == True):
                    try:
                        self.tcp_s.shutdown(socket.SHUT_RDWR)
                        self.tcp_s.close()
                        self.tcp_conn_status = False
                        self.guiMessage = 1
                    except:
                        self.tcp_s.close()
                        self.tcp_conn_status = False
                        self.guiMessage = 1
                break

    def disconnect(self):
        try:
            self.tcp_s.send(bytes("LEAV", 'UTF-8'))
            recv = self.tcp_s.recv(1024)
            decoded = recv.decode('UTF-8')
            if(decoded == 'BYE'):
                self.tcp_s.shutdown(socket.SHUT_RDWR)
                self.tcp_s.close()
            self.tcp_conn_status = False
        except:
            self.tcp_s.close()
            self.tcp_conn_status = False
        print("disconnected")

    def Start(self, nick, server_addr, server_tcp_port):
        self.sockets_setup()
        self.set_nick(nick)
        self.set_server_addr(server_addr)
        self.set_server_tcp_port(server_tcp_port)
        self.muted = False
        self.usersList = []
        print('connecting')
        self.tcp_s.connect((self.server_address, self.server_tcp_port))
        print('connected')
        Thread(target=self.tcpConnection).start()

if (__name__ == "__main__"):
    client = Client()
    client.Start('Tester', '127.0.0.1', 5001)
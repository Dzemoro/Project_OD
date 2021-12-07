from sys import path
from typing import List
if '' not in path:
    path.append('')

import socket
from threading import Thread
from contextlib import closing
import re, sys, time, os
from common.message_type import MessageType
from common.user import User
from enum import Enum
        
class Server:
    def __init__(self, ip, tcp_port):
        if(ip.lower() == 'auto' or ip == ''):
            self.ip = socket.gethostbyname(socket.gethostname())
        else:
            self.ip = ip

        if(tcp_port.lower() == 'auto' or tcp_port == ''):
            self.server_tcp_port = 0
        else:
            self.server_tcp_port = int(tcp_port)
        
        self.userList = []

        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_s.bind((self.ip, self.server_tcp_port))
        self.server_tcp_port = self.tcp_s.getsockname()[1]

        self.udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_s.bind((self.ip, 0))

        print("Server is listening on "+self.ip+':'+str(self.server_tcp_port)+" ...")
        self.userConnections()

    def userConnections(self):
            self.tcp_s.listen(25)
            while True:
                conn, address = self.tcp_s.accept()
                data = conn.recv(1024) #messages: JOIN Nick; AWLI; LEAV; GIVE Nick;
                decoded = data.decode('UTF-8')
                message = decoded.split()
                if(message[0] == 'JOIN' and len(message[1]) > 0):
                    
                    user = User(conn, message[1], address, int(message[2]))
                    self.userList.append(user)

                    #create udp socket for user
                    #user_udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    #user_udp_s.bind((self.ip, 0))

                    #send OK with udp port for audio communication
                    conn.send(bytes('OK', 'UTF-8'))
                    #print("\n"+user.udpAddr[0]+" User "+user.name+" joined server")
                    #print("  TCP: "+str(user.tcpAddr[1])+" <-> "+str(self.server_tcp_port))
                    #print("  UDP: "+str(user.udpAddr[1])+" <-> "+str(user_udp_s.getsockname()[1]))
                    
                    Thread(target=self.newConnection, args=(conn, user)).start()
                    #Thread(target=self.audioStreaming, args=(user_udp_s, user)).start()
                else:
                    print('\nReceived bad data: '+decoded+' from: '+str(address[0])+':'+str(address[1]))
                    conn.send(bytes('BAD DATA', 'UTF-8'))
                    conn.close()

    def newConnection(self, conn, user):
            while True:
                try:
                    data = conn.recv(1024)
                    decoded = data.decode('UTF-8')
                    message = decoded.split()
                    if(message[0] == 'LEAV'):
                        self.userList.remove(user)
                        conn.send(bytes('BYE', 'UTF-8'))
                        print("\nUser "+user.name+" disconnected peacefully")
                        break
                    elif(message[0] == 'AWLI'):
                        message = 'LIST'
                        for u in self.userList:
                            message += ' '+str(u.name)
                        conn.send(bytes(message, 'UTF-8'))
                        
                        #TODO wysłanie IP wybranego usera
                    elif(message[0] == 'GIVE' and len(message[1]) > 0):
                        #szukanie po nazwie usera
                        #print('give')
                        message = 'IP'
                        usrname = message[1]
                        for u in self.userList:
                            if (u.name == usrname):
                                message += ' '+str(u.tcpAddr)
                        conn.send(bytes(message, 'UTF-8'))

                except socket.error:
                    try:
                        print("\nUser "+user.name+" disconnected forcibly")
                        self.userList.remove(user)
                        conn.close()
                        break
                    except:
                        break
    
    def identify_message_type(self, data):
        if isinstance(MessageType[data], MessageType):
            return MessageType[data]
        else:
            raise Exception('Unknown message type')
    
    def handle_message(self, type : MessageType, data, conn, address):
        user = User(conn, '', address)
        if type is MessageType.JOIN:
            #user = User(conn, data[1], address)
            self.userList.append(user)
            #send OK with udp port for audio communication
            conn.send(bytes('OK', 'UTF-8'))
            Thread(target=self.newConnection, args=(conn, user)).start()
        elif type is MessageType.LIST:
            message = 'LIST'
            for u in self.userList:
                message += ':'+str(u.name)
            conn.send(bytes(message, 'UTF-8'))
        elif type is MessageType.QUIT:
            self.userList.remove(user)
            conn.send(bytes('BYE', 'UTF-8'))
            print("\nUser "+user.name+" disconnected peacefully")
        else:
            print('\nReceived invalid data from: '+str(address[0])+':'+str(address[1]))
            conn.send(bytes('BAD DATA', 'UTF-8'))
            conn.close()


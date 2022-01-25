from base64 import decode
from email import message
from re import T
import sys, os, threading, socket

import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from client import Client
from stylesheets import *
from chatGui import ChatWindow

from encrypting.fernet import FernetCipher
from encrypting.caesarCipher import CaesarCipher
from encrypting.polybiusSquareCipher import PolybiusSquareCipher
from encrypting.RagBabyCipher import RagBabyCipher

class PhonebookWindow(QMainWindow):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def __init__(self, *args, **kwargs):
        super(PhonebookWindow, self).__init__(*args, *kwargs)
        self.setWindowTitle("Komunikator")
        self.setWindowIcon(QIcon(self.imgPath + "window_icon.png"))

        self.timer1 = QTimer()
       
        self.contentLayout = QtWidgets.QVBoxLayout()

        self.titleLabel = QtWidgets.QLabel()
        self.titleLabel.setStyleSheet(phonebookLabelStyle)
        self.titleLabel.setText("Witaj!\nZ kim chcesz porozmawiać?")

        self.logoutButton = QtWidgets.QPushButton()
        self.logoutButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.logoutButton.setFixedSize(QtCore.QSize(120, 30))
        self.logoutButton.setStyleSheet(buttonStyle)
        self.logoutButton.setText("Wyloguj się")
        self.logoutButton.clicked.connect(self.handleLogoutClick)

        self.refreshButton = QtWidgets.QPushButton()
        self.refreshButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.refreshButton.setFixedSize(QtCore.QSize(120, 30))
        self.refreshButton.setStyleSheet(buttonStyle)
        self.refreshButton.setText("Odśwież listę")
        self.refreshButton.clicked.connect(self.handleRefreshClick)

        self.connectButton = QtWidgets.QPushButton()
        self.connectButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.connectButton.setFixedSize(QtCore.QSize(120, 30))
        self.connectButton.setStyleSheet(buttonStyle)
        self.connectButton.setText("Połącz")
        self.connectButton.clicked.connect(self.handleConnectClick)

        self.buttonLayout = QtWidgets.QGridLayout()
        self.buttonLayout.addWidget(self.logoutButton, 0, 1)
        self.buttonLayout.addWidget(self.refreshButton, 1, 0)
        self.buttonLayout.addWidget(self.connectButton, 1, 1)
        self.buttonLayoutW = QWidget()
        self.buttonLayoutW.setLayout(self.buttonLayout)

        self.upperLayout = QtWidgets.QHBoxLayout()
        self.upperLayout.addWidget(self.titleLabel)
        self.upperLayout.addWidget(self.buttonLayoutW)
        self.upperLayoutW = QWidget()
        self.upperLayoutW.setLayout(self.upperLayout)
        
        self.areaScrollBar = QtWidgets.QScrollBar()
        self.areaScrollBar.setStyleSheet(scrollBarStyle)

        self.usersArea = QtWidgets.QListWidget()
        self.usersArea.setStyleSheet(usersAreaStyle)
        self.usersArea.setFixedHeight(670)
        self.usersArea.setVerticalScrollBar(self.areaScrollBar)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.upperLayoutW)
        self.mainLayout.addWidget(self.usersArea)

        mainW = QWidget()
        mainW.setLayout(self.mainLayout)
        self.setCentralWidget(mainW)

        self.caesar = CaesarCipher()
        self.fernet = FernetCipher()
        self.polybius = PolybiusSquareCipher()
        self.rag_baby = RagBabyCipher()

        self.myUsername = ""
        self.friend_name = ""
        self.isCall = False
        self.imCalling = False
        self.receiveThread = None



        self.timer1.timeout.connect(self.listenIsCall)
        self.timer1.start()

    def handleLogoutClick(self):
        msg = "QUIT"
        self.client.conn.send(msg.encode('utf-8'))
        received = self.client.conn.recv(1024).decode('utf-8') #tego tu nie powinno byc bo recv 
        if received == "SPOX":
            import loginGui
            self.loginWindow = loginGui.LoginWindow()
            self.loginWindow.open()
            self.close()

    def handleRefreshClick(self):
        msg = "LIST"
        self.client.conn.send(msg.encode('utf-8'))
        # received = self.client.conn.recv(1024)
        # users = received.decode().split(":")
        # del users[0]
        # self.addUsersToList(users)

    def handleConnectClick(self):
        if len(self.usersArea.selectedItems()) == 1:
            chosen_friend_name = str(self.usersArea.selectedItems()[0].text())
            msg = "CONN:" + chosen_friend_name
            self.client.conn.send(msg.encode('utf-8'))
            self.imCalling = True

            self.openChatWindow()

            # received = self.client.conn.recv(1024).decode('utf-8')
            # message = received.split(":")
            # received_message_type = message[0]

            # if received_message_type == "SPOX":
            #     self.friend_name = message[1]
            #     self.openChatWindow()  

            # elif received_message_type == "DENY": #TODO deny ogarnac
            #     pass
    
    @pyqtSlot()         
    def openChatWindow(self):
        self.chatWindow = ChatWindow()
        #self.chatWindow.friend = friend
        self.chatWindow.myUsername = self.myUsername
        self.chatWindow.friendUsername = self.friend_name
        self.chatWindow.client = self.client
        self.chatWindow.open()
        self.close()

    def setMyUsername(self):
        self.titleLabel.setText("Witaj, " + str(self.myUsername) + "!\nZ kim chcesz porozmawiać?")
    
    @pyqtSlot()           
    def open(self):

        self.receiveThread = threading.Thread(target=self.receiveServerData)
        self.receiveThread.setDaemon(True)
        self.receiveThread.start()  

        self.setFixedSize(600, 800)
        self.setStyleSheet(dialogStyle)
        if self.myUsername != "":
            self.setMyUsername()
        #self.handleRefreshClick()
        self.show()   

    @pyqtSlot()              
    def listenIsCall(self):
        if self.isCall == True:
            self.openChatWindow()
            self.isCall = False                

            self.receiveThread = threading.Thread(target=self.receiveServerData)
            self.receiveThread.setDaemon(True)
            self.receiveThread.start()
          
    @pyqtSlot()              
    def receiveServerData(self):
        while True:
            #time.sleep(3)
            received = self.client.conn.recv(1024)
            print(received)
            if received != b'':

                message = received.decode('utf-8').split(":")
                print(message)

                received_message_type = message[0]
                if received_message_type == "CALL": #odbieram zgadzam sie 
                    self.friend_name = message[1]
                    keys = self.generate_keys()   
                    msg = "KEYS:" + message[1] + keys  

                    message = msg.split(":")

                    ChatWindow.my_caesarKey = message[2]
                    ChatWindow.my_fernetKey = message[3]
                    ChatWindow.my_polybiusKey = message[4]
                    ChatWindow.my_ragbabyKey = message[5]                  ##mess:target:cezar:fernet:polybius:rag_baby 

                    self.client.conn.send(msg.encode('utf-8'))
                elif received_message_type == "CONN": #ja dzwonie
                    msg = "CALL:" + message[1]
                    self.client.conn.send(msg.encode('utf-8'))
                    self.friend_name = message[1]
                    self.isCall = True 
                    break                   
                elif received_message_type == "LIST":
                    users = received.decode().split(":")
                    del users[0]
                    self.addUsersToList(users)  
                elif received_message_type == "MESS":
                    message_content = message[2]
                    decode_type = message[3]

                    decrypted = self.decrypt_message(message_content, decode_type)
                    
                    self.chatWindow.printMessage(message[1], decrypted)       
  
                elif received_message_type == "KEYS": 
                    self.friend_name = message[1]
                    keys = self.generate_keys()

                    msg = "KEYR:" + message[1] + keys   

                    splitted_keys = keys.split(":")

                    ChatWindow.my_caesarKey = splitted_keys[0]
                    ChatWindow.my_fernetKey = splitted_keys[1]
                    ChatWindow.my_polybiusKey = splitted_keys[2]
                    ChatWindow.my_ragbabyKey = splitted_keys[3] 
                         
                    
                    ChatWindow.friend_caesarKey = message[2]
                    ChatWindow.friend_fernetKey = message[3]
                    ChatWindow.friend_polybiusKey = message[4]
                    ChatWindow.friend_ragbabyKey = message[5]
                    
                    self.client.conn.send(msg.encode('utf-8'))#czyszczenie kluczy przy rozlaczeniu 
                elif received_message_type == "KEYR": 
                    self.friend_name = message[1]

                    ChatWindow.friend_caesarKey = message[2]
                    ChatWindow.friend_fernetKey = message[3]
                    ChatWindow.friend_polybiusKey = message[4]
                    ChatWindow.friend_ragbabyKey = message[5]
                
                elif received_message_type == "LEAV":
                    self.isCall = False
                    msg = "LEAR:" + self.friend_name
                    self.client.conn.send(msg.encode('utf-8'))
                    break
                
                elif received_message_type == "LEAR":
                    self.isCall = False
                    break
                                   
                elif received_message_type == "QUIT":
                    pass

    def decrypt_message(self, message_content, decode_type):

        if decode_type == "CA":
            return self.caesar.decrypt(key = self.friend_caesarKey, message = message_content)
        elif decode_type == "FE":
            return self.fernet.decrypt(key = self.friend_fernetKey, message = message_content)
        elif decode_type == "PO":
            return self.polybius.decrypt(key = self.friend_polybiusKey, word = message_content)
        elif decode_type == "RA":
            return self.rag_baby.decrypt(key = self.friend_ragbabyKey, text = message_content)
        elif decode_type == "NO":
            return message_content


    def generate_keys(self):
        caesar_key = self.caesar.gen_key()
        fernet_key = self.fernet.gen_key()
        polybius_key = self.polybius.gen_key()
        rag_baby_key = self.rag_baby.gen_key()
        return ":" + str(caesar_key) + ":" + str(fernet_key) + ":" + str(polybius_key) + ":" + str(rag_baby_key)

    def sendDataToClient(self):
        while True:
            try:
                if self.sendFlag:
                    data = self.recordingStream.read(1024)
                    self.s.sendall(data)
            except:
                self.handleServerDis()
                break

    def sendInitialDataToClient(self, ipaddr, port, nickname):
        try:
            #conn
            if self.sendFlag:
                data = self.recordingStream.read(1024)
                self.s.sendall(data)
        except:
            self.handleServerDis()
        
    def addUsersToList(self, usernames):
        self.usersArea.clear()
        if isinstance(usernames, str):
            usernames=[usernames]
        self.usersArea.addItems(usernames)

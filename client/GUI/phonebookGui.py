import sys, os, threading, socket, time


from encrypting.fernet import FernetCipher
from encrypting.caesarCipher import CaesarCipher
from encrypting.polybiusSquareCipher import PolybiusSquareCipher
from encrypting.RagBabyCipher import RagBabyCipher

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from client import *
from stylesheets import *
from chatGui import *

class PhonebookWindow(QMainWindow):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def __init__(self, *args, **kwargs):
        super(PhonebookWindow, self).__init__(*args, *kwargs)
        self.setWindowTitle("Komunikator")
        self.setWindowIcon(QIcon(self.imgPath + "window_icon.png"))
       
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

        self.caesar = CaesarCipher()
        self.fernet = FernetCipher()
        self.polybius = PolybiusSquareCipher()
        self.rag_baby = RagBabyCipher()

        mainW = QWidget()
        mainW.setLayout(self.mainLayout)
        self.setCentralWidget(mainW)

        self.myUsername = ""


    def handleLogoutClick(self):
        msg = "QUIT"
        self.client.conn.send(msg.encode())
        received = self.client.conn.recv(1024).decode()
        if received == "SPOX":
            import loginGui
            self.loginWindow = loginGui.LoginWindow()
            self.loginWindow.open()
            self.close()

    def handleRefreshClick(self):
        msg = "LIST"
        self.client.conn.send(msg.encode())
        received = self.client.conn.recv(1024).decode()
        users = received.split(":")
        del users[0]
        self.addUsersToList(users)

    def handleConnectClick(self):
        if len(self.usersArea.selectedItems()) == 1:
            chosen_friend_name = str(self.usersArea.selectedItems()[0].text())
            msg = "GIVE:" + chosen_friend_name
            self.client.conn.send(msg.encode())

            received = self.client.conn.recv(1024).decode()
            friend_params = received.split(":")
            received_message_type = friend_params[0]
            friends_name = friend_params[1]

            # TODO Rzeczy różne niestworzone
            if received_message_type == "GIVE":
                friends_ip = friend_params[2]
                friends_port = friend_params[3]
                message = 'CONN:' + self.myUsername
                message_bytes = str.encode(message)

                self.client.conn.send(message_bytes)

            elif received_message_type == "DENY": #TODO deny ogarnac
                pass

    def openChatWindow(self):
        self.chatWindow = ChatWindow()
        #self.chatWindow.friend = friend
        self.chatWindow.myUsername = self.myUsername
        self.chatWindow.client = self.client
        self.chatWindow.open()
        self.close()

    def setMyUsername(self):
        self.titleLabel.setText("Witaj, " + str(self.myUsername) + "!\nZ kim chcesz porozmawiać?")

    def open(self):
        self.setFixedSize(600, 800)
        self.setStyleSheet(dialogStyle)
        if self.myUsername != "":
            self.setMyUsername()

        threading.Thread(target=self.client.receive).start()
        time.sleep(2)
                        
        self.handleRefreshClick()
        self.show()


    def receiveClientData(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', 0))

        while True:
            try:
                conn, addr = self.sock.accept()
                wrap = self.context.wrap_socket(conn, server_hostname=str(conn))
                data = self.s.recv(1024)

                if bytes("CONN:".encode('utf-8')) in data:
                    conn.send("SPOX")
                    self.openChatWindow()
                elif bytes("SPOX".encode('utf-8')) in data:
                    self.openChatWindow() 

            except Exception as e:
                print(e)
                break

    def exchange_keys(self):
        caesar_key = self.caesar.gen_key()
        fernet_key = self.fernet.gen_key()
        polybius_key = self.polybius.gen_key()
        rag_baby_key = self.rag_baby.gen_key()
        keys = str(caesar_key) + ":" + str(fernet_key) + ":" + str(polybius_key) + ":" + str(rag_baby_key)

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

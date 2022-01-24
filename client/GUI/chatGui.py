import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import Client
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from encrypting.fernet import FernetCipher
from encrypting.caesarCipher import CaesarCipher
from encrypting.polybiusSquareCipher import PolybiusSquareCipher
from encrypting.RagBabyCipher import RagBabyCipher

from stylesheets import *

class ChatWindow(QMainWindow):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def __init__(self, *args, **kwargs):
        super(ChatWindow, self).__init__(*args, *kwargs)
        self.setWindowTitle("Komunikator")
        self.setWindowIcon(QIcon(self.imgPath + "window_icon.png"))

        self.contentLayout = QtWidgets.QVBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setObjectName("contentLayout")

        self.disconnectButton = QtWidgets.QPushButton()
        self.disconnectButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.disconnectButton.setFixedSize(QtCore.QSize(120, 30))
        self.disconnectButton.setStyleSheet(buttonStyle)
        self.disconnectButton.setText("Rozłącz się")
        self.disconnectButton.clicked.connect(self.handleDisconnectClick)
        self.contentLayout.addWidget(self.disconnectButton, alignment=QtCore.Qt.AlignRight)
        
        self.encryptDropDown = QtWidgets.QComboBox()
        self.encryptDropDown.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.encryptDropDown.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.encryptDropDown.setStyleSheet(encryptDropDownStyle)
        self.encryptDropDown.setEditable(False)
        self.encryptDropDown.setObjectName("encryptDropDown")
        self.encryptDropDown.addItem("Bez szyfrowania")
        self.encryptDropDown.addItem("Fernet") #jest taki likier dx 
        self.encryptDropDown.addItem("RagBaby") #szmaciane dziecko
        self.encryptDropDown.addItem("Szyfr Cezara") #krul i wladca
        self.encryptDropDown.addItem("Szyfr Polibiusza") #kogo 
        # self.encryptDropDown.setMaxVisibleItems(11)
        self.encryptDropDown.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.encryptDropDown.view().setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.encryptDropDown.activated[str].connect(self.handleItemDropdown)
        self.contentLayout.addWidget(self.encryptDropDown)
        
        self.areaScrollBar = QtWidgets.QScrollBar()
        self.areaScrollBar.setStyleSheet(scrollBarStyle)

        self.messagesArea = QtWidgets.QTextBrowser()
        self.messagesArea.setStyleSheet(messagesAreaStyle)
        self.messagesArea.setFixedHeight(630)
        self.messagesArea.setVerticalScrollBar(self.areaScrollBar)
        self.contentLayout.addWidget(self.messagesArea)
        
        self.bottomLayout = QtWidgets.QHBoxLayout()  

        self.inputScrollBar = QtWidgets.QScrollBar()
        self.inputScrollBar.setStyleSheet(scrollBarStyle)
        
        self.messageInput = QtWidgets.QTextEdit()
        self.messageInput.setMinimumSize(QtCore.QSize(470, 60))
        self.messageInput.setMaximumSize(QtCore.QSize(470, 60))
        self.messageInput.setToolTip("")
        self.messageInput.setStyleSheet(messageInputStyle)
        self.messageInput.setVerticalScrollBar(self.inputScrollBar)
        self.bottomLayout.addWidget(self.messageInput, alignment=QtCore.Qt.AlignLeft)
        
        self.sendButton = QtWidgets.QPushButton()
        self.sendButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.sendButton.setMinimumSize(QtCore.QSize(100, 30))
        self.sendButton.setMaximumSize(QtCore.QSize(100, 30))
        self.sendButton.setStyleSheet(sendButtonStyle)
        self.sendButton.setText("Wyślij")
        self.sendButton.clicked.connect(self.handleSendClick)
        self.bottomLayout.addWidget(self.sendButton)

        self.contentLayout.addLayout(self.bottomLayout)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.contentLayout)

        mainW = QWidget()
        mainW.setLayout(self.mainLayout)
        self.setCentralWidget(mainW)

        self.myUsername = ""
        self.friendUsername = ""
        self.lastMessageAuthorIsMe = False

        self.caesar = CaesarCipher()
        self.fernet = FernetCipher()
        self.polybius = PolybiusSquareCipher()
        self.rag_baby = RagBabyCipher()

        self.my_caesarKey = ""
        self.my_fernetKey = ""
        self.my_polybiusKey = ""
        self.my_ragbabyKey = ""            
        
        self.friend_caesarKey = ""
        self.friend_fernetKey = ""
        self.friend_polybiusKey = ""
        self.friend_ragbabyKey = ""

    def handleSendClick(self):
        if self.messageInput.toPlainText() and not self.messageInput.toPlainText().isspace():

            message_content = self.messageInput.toPlainText()
            encrypted_message, encrypt_type = self.encrypt_message(message_content, str(self.encryptDropDown.currentText())) ##castowanie dla jaj
            print(message_content)
            msg = "MESS:" + self.friendUsername + ":" + encrypted_message + ":" + encrypt_type
            self.client.conn.send(msg.encode('utf-8'))

            self.printMessage(self.myUsername, self.messageInput.toPlainText())
        self.messageInput.clear()

    def encrypt_message(self, message_content, encode_type):

        if encode_type == "Szyfr Cezara":
            return self.caesar.encrypt(key = self.my_caesarKey, message = message_content), "CA"
        elif encode_type == "Fernet":
            return self.fernet.encrypt(key = self.my_fernetKey, message = message_content), "FE"
        elif encode_type == "Szyfr Polibiusza":
            return self.polybius.encrypt(key = self.my_polybiusKey, word = message_content), "PO"
        elif encode_type == "RagBaby":
            return self.rag_baby.encrypt(key = self.my_ragbabyKey, text = message_content), "RA"

    def handleDisconnectClick(self):
        # TODO Rzeczy różne niestworzone
        import phonebookGui
        self.phonebookWindow = phonebookGui.PhonebookWindow()
        self.phonebookWindow.myUsername = self.myUsername
        self.phonebookWindow.client = self.client
        self.phonebookWindow.open()
        self.close()

    def handleItemDropdown(self, encryptType):
        # TODO Rzeczy różne niestworzone
        self.printInfo("Zmieniono szyfrowanie na: " + str(encryptType))

    def printMessage(self, sender, message):
        if not self.lastMessageAuthorIsMe:
            username = "<span style=\"color:#FFBC97;\" >"
            username += str(sender)
            username += "</span>"
            self.messagesArea.append(username)
            self.lastMessageAuthorIsMe = True

        self.messagesArea.append(str(message))
    
    def printInfo(self, message):
        info = "<span style=\"color:#FFBC97;\" >"
        info += "--- "+str(message)+" ---"
        info += "</span>"
        self.messagesArea.append(info)
        self.lastMessageAuthorIsMe = False

    def open(self):
        self.setFixedSize(600, 800)
        self.setStyleSheet(dialogStyle)
        self.printInfo("Połączono z " + str(self.friendUsername))
        self.show()

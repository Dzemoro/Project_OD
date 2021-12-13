import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.encryptDropDown.addItem("Inna opcja")
        self.encryptDropDown.addItem("Inna opcja 2")
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

    def handleSendClick(self):
        if self.messageInput.toPlainText() and not self.messageInput.toPlainText().isspace():
            # TODO Rzeczy różne niestworzone
            self.printMessage(self.myUsername, self.messageInput.toPlainText())
        self.messageInput.clear()

    def handleDisconnectClick(self):
        # TODO Rzeczy różne niestworzone
        import phonebookGui
        self.phonebookWindow = phonebookGui.PhonebookWindow()
        self.phonebookWindow.myUsername = self.myUsername
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

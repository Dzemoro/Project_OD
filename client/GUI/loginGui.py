import sys, path, os, asyncio, threading

from usernames import is_safe_username

from client import Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from stylesheets import *

from phonebookGui import *

class LoginWindow(QMainWindow):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, *kwargs)
        self.setWindowTitle("Komunikator")
        self.setWindowIcon(QIcon(self.imgPath + "window_icon.png"))

        self.inputsLayout = QtWidgets.QFormLayout()

        self.ipLayout = QtWidgets.QFormLayout()
        self.ipLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.ipLabel = QtWidgets.QLabel()
        self.ipLabel.setFixedSize(QtCore.QSize(50, 30))
        self.ipLabel.setStyleSheet(labelStyle)
        self.ipLabel.setText("IP:")
        self.ipLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ipLabel)
        
        self.ipInput = QtWidgets.QLineEdit()
        self.ipInput.setFixedSize(QtCore.QSize(200, 30))
        self.ipInput.setStyleSheet(inputStyle)
        self.ipLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ipInput)
        self.inputsLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.ipLayout)

        self.portLayout = QtWidgets.QFormLayout()
        self.portLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.portLabel = QtWidgets.QLabel()
        self.portLabel.setFixedSize(QtCore.QSize(50, 30))
        self.portLabel.setStyleSheet(labelStyle)
        self.portLabel.setText("Port:")
        self.portLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.portLabel)
        
        self.portInput = QtWidgets.QLineEdit()
        self.portInput.setFixedSize(QtCore.QSize(200, 30))
        self.portInput.setStyleSheet(inputStyle)
        self.portLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.portInput)
        self.inputsLayout.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.portLayout)

        self.nickLayout = QtWidgets.QFormLayout()
        self.nickLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.nickLabel = QtWidgets.QLabel()
        self.nickLabel.setFixedSize(QtCore.QSize(50, 30))
        self.nickLabel.setStyleSheet(labelStyle)
        self.nickLabel.setText("Nick:")
        self.nickLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nickLabel)
        
        self.nickInput = QtWidgets.QLineEdit()
        self.nickInput.setFixedSize(QtCore.QSize(200, 30))
        self.nickInput.setStyleSheet(inputStyle)
        self.nickLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nickInput)
        self.inputsLayout.setLayout(2, QtWidgets.QFormLayout.LabelRole, self.nickLayout)
        
        self.startBtn = QtWidgets.QPushButton()
        self.startBtn.setFixedSize(QtCore.QSize(120, 40))
        self.startBtn.setStyleSheet(buttonStyle)
        self.startBtn.setText("DOŁĄCZ")
        self.startBtn.clicked.connect(self.handleLoginClick)

        self.inputsLayoutW = QWidget()
        self.inputsLayoutW.setLayout(self.inputsLayout)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(self.inputsLayoutW, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.startBtn, alignment=Qt.AlignHCenter)

        mainW = QWidget()
        mainW.setLayout(self.mainLayout)
        self.setCentralWidget(mainW)

    def handleLoginClick(self):
        if self.checkInputs():
            client = Client(self.ipInput.text(),int(self.portInput.text()))

            msg = "JOIN:" + self.nickInput.text()
            client.conn.send(msg.encode('utf-8'))
            receive = client.conn.recv(1024).decode('utf-8')
            if receive == 'SPOX':
                self.phonebookWindow = PhonebookWindow()
                self.phonebookWindow.myUsername = self.nickInput.text()
                self.phonebookWindow.client = client
                self.phonebookWindow.open()
                self.close()
            elif receive == 'DENY':
                pass


    def open(self):
        self.setFixedSize(341, 210)
        self.setStyleSheet(dialogStyle)
        self.show()

    def checkInputs(self):
        if self.checkPort(self.portInput.text()) is not True and self.checkIp(self.ipInput.text()) is not True and self.checkNick(self.nickInput.text()) is not True:    
            self.portInput.setText("Wrong port number!")
            self.ipInput.setText("Wrong IP address!")
            self.nickInput.setText("Wrong nickname!")     
            return False
        elif self.checkIp(self.ipInput.text()) is not True: 
            self.ipInput.setText("Wrong IP address!")  
            return False
        elif self.checkPort(self.portInput.text()) is not True:  
            self.portInput.setText("Wrong port number!")
            return False
        elif self.checkNick(self.nickInput.text()) is not True:
            self.nickInput.setText("Wrong nickname!")     
            return False
        return True

    def checkIp(self, ipAddr):
        def partCheck(ipAddr):
            try: return str(int(ipAddr)) == ipAddr and 0 <= int(ipAddr) <= 255
            except: return False
        if ipAddr.count(".") == 3 and all(partCheck(i) for i in ipAddr.split(".")):
            return True

    def checkPort(self, port):
        if port == "":
            return False
        if all(d.isdigit() for d in port): # and (int(port) >= 29200 and int(port) <= 65000):
            return True
        return False

    def checkNick(self, nick):
        return is_safe_username(nick)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.open()
    app.exec_()
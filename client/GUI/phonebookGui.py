import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from stylesheets import *
from chatGui import *

class PhonebookWindow(QMainWindow):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def __init__(self, *args, **kwargs):
        super(PhonebookWindow, self).__init__(*args, *kwargs)
        self.setWindowTitle("Komunikator")
        self.setWindowIcon(QIcon(self.imgPath + "window_icon.png"))
       
        self.contentLayout = QtWidgets.QVBoxLayout()
        
        self.connectButton = QtWidgets.QPushButton()
        self.connectButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.connectButton.setFixedSize(QtCore.QSize(100, 30))
        self.connectButton.setStyleSheet(connectButtonStyle)
        
        self.areaScrollBar = QtWidgets.QScrollBar()
        self.areaScrollBar.setStyleSheet(scrollBarStyle)

        self.usersArea = QtWidgets.QTextBrowser()
        self.usersArea.setStyleSheet(messagesAreaStyle)
        self.usersArea.setFixedHeight(650)
        self.usersArea.setObjectName("messagesArea")
        self.usersArea.setVerticalScrollBar(self.areaScrollBar)

        self.connectButton.setText("Połącz")
        self.connectButton.clicked.connect(self.handleConnectClick)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.connectButton, alignment=QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.usersArea)

        mainW = QWidget()
        mainW.setLayout(self.mainLayout)
        self.setCentralWidget(mainW)

    def handleConnectClick(self):
        # TODO Rzeczy różne niestworzone
        if True:
            self.chatWindow = ChatWindow()
            self.chatWindow.open()
            self.close()

    def open(self):
        self.setFixedSize(600, 800)
        self.setStyleSheet(dialogStyle)
        self.show()

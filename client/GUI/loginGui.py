import sys, path, os, asyncio, threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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
        self.nickLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nickLabel)
        
        self.nickInput = QtWidgets.QLineEdit()
        self.nickInput.setFixedSize(QtCore.QSize(200, 30))
        self.nickInput.setStyleSheet(inputStyle)
        self.nickLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nickInput)
        self.inputsLayout.setLayout(2, QtWidgets.QFormLayout.LabelRole, self.nickLayout)
        
        self.startBtn = QtWidgets.QPushButton()
        self.startBtn.setFixedSize(QtCore.QSize(120, 40))
        self.startBtn.setStyleSheet(startBtnStartStyle)
        self.startBtn.clicked.connect(self.handleLoginClick)
        
        self.ipLabel.setText("IP:")
        self.portLabel.setText("Port:")
        self.nickLabel.setText("Nick:")
        self.startBtn.setText("DOŁĄCZ")
        self.startBtn.setCheckable(True) 

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
        # TODO Rzeczy różne niestworzone
        if True:
            self.phonebookWindow = PhonebookWindow()
            self.phonebookWindow.open()
            self.close()

    def open(self):
        self.setFixedSize(341, 210)
        self.setStyleSheet(dialogStyle)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.open()

    app.exec_()
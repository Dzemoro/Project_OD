import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QIcon

from clientGuiMethods import *
from stylesheets import *

class Ui_Dialog(object):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(600, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        Dialog.setStyleSheet(dialogStyle)
        Dialog.setFixedSize(Dialog.size())
        Dialog.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        Dialog.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        Dialog.setWindowIcon(QIcon(self.imgPath + "window_icon.png"))

        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 581, 781))
        self.layoutWidget.setObjectName("layoutWidget")
       
        self.contentLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setObjectName("contentLayout")
        
        self.encryptDropDown = QtWidgets.QComboBox(self.layoutWidget)
        self.encryptDropDown.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.encryptDropDown.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.encryptDropDown.setStyleSheet(encryptDropDownStyle)
        self.encryptDropDown.setEditable(False)
        self.encryptDropDown.setObjectName("encryptDropDown")
        self.encryptDropDown.addItem("Bez szyfrowania")
        self.encryptDropDown.addItem("Inna opcja")
        self.encryptDropDown.addItem("Inna opcja 2")
        self.encryptDropDown.setMaxVisibleItems(11)
        self.encryptDropDown.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.encryptDropDown.view().setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.contentLayout.addWidget(self.encryptDropDown)
        
        self.areaScrollBar = QtWidgets.QScrollBar()
        self.areaScrollBar.setStyleSheet(scrollBarStyle)

        self.messagesArea = QtWidgets.QTextBrowser(self.layoutWidget)
        self.messagesArea.setStyleSheet(messagesAreaStyle)
        self.messagesArea.setFixedHeight(650)
        self.messagesArea.setObjectName("messagesArea")
        self.messagesArea.setVerticalScrollBar(self.areaScrollBar)
        self.contentLayout.addWidget(self.messagesArea)
        
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.setObjectName("bottomLayout")        

        self.inputScrollBar = QtWidgets.QScrollBar()
        self.inputScrollBar.setStyleSheet(scrollBarStyle)
        
        self.messageInput = QtWidgets.QTextEdit(self.layoutWidget)
        self.messageInput.setMinimumSize(QtCore.QSize(470, 60))
        self.messageInput.setMaximumSize(QtCore.QSize(470, 60))
        self.messageInput.setToolTip("")
        self.messageInput.setStyleSheet(messageInputStyle)
        self.messageInput.setObjectName("messageInput")
        self.messageInput.setVerticalScrollBar(self.inputScrollBar)
        self.bottomLayout.addWidget(self.messageInput, alignment=QtCore.Qt.AlignLeft)
        
        self.sendButton = QtWidgets.QPushButton(self.layoutWidget)
        self.sendButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.sendButton.setMinimumSize(QtCore.QSize(100, 30))
        self.sendButton.setMaximumSize(QtCore.QSize(100, 30))
        self.sendButton.setStyleSheet(sendButtonStyle)
        self.sendButton.setObjectName("sendButton")
        self.bottomLayout.addWidget(self.sendButton)

        self.contentLayout.addLayout(self.bottomLayout)
   
        self.sendButton.setCheckable(True) 

        #methods mapping
        Ui_Dialog.handleClick = handleClick
        Ui_Dialog.handleItemDropdown = handleItemDropdown

        self.sendButton.clicked.connect(self.handleClick)
        self.encryptDropDown.activated[str].connect(self.handleItemDropdown)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Komunikator"))
        self.sendButton.setText("Wyślij")

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

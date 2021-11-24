import sys, path, os, asyncio, threading, socket, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtGui, QtWidgets

#TODO
def handleClick(self):
    self.messagesArea.append(self.messageInput.toPlainText())
    self.messageInput.clear()

#TODO
def handleItemDropdown(self):
    pass
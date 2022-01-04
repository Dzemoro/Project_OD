from socket import socket
from common.message_type import MessageType

class Message:
    def __init__(self, format):
        self.format = format

    def receive(self, conn : socket):
        data = conn.recv(1024)
        decoded = data.decode(self.format)
        message = decoded.split(':')
        return message

    def send(self, message : str, conn : socket):
        message_in_bytes = bytes(message, self.format)
        conn.send(message_in_bytes)

    def identify_message_type(self, data):
        if data in MessageType.__members__:
            return MessageType[data]
        else:
            return MessageType.DENY
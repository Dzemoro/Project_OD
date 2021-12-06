from socket import socket

class Message:
    def __init__(self, format):
        self.format = format

    def receive(self, data : bytes, conn : socket):
        decoded = data.decode(self.format)
        message = decoded.split(':')
        return message

    def send(self, message : str, conn : socket):
        message_in_bytes = bytes(message, self.format)
        conn.send(message_in_bytes)
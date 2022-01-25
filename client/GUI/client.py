from sys import path
from typing import Dict
if '' not in path:
    path.append('')

import socket
import ssl

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile=r"./client/GUI/cert.pem")
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.conn = self.context.wrap_socket(self.client, server_hostname=str(self.ip))
        self.conn.connect((str(ip), int(port)))        

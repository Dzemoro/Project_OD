import socket
import ssl

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile="C:\\Users\\mciec\\Desktop\\Studia\\OD\\Project_OD\\server\\src\\cert.pem")
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.conn = self.context.wrap_socket(self.client, server_hostname=str(self.ip))
        self.conn.connect((str(ip), int(port)))        


# if __name__ == "__main__":
##     #conn.bind((HOST, PORT))
#     conn.connect(('127.0.0.1',60000))
#     run = True
#     while run:
#         msg = input()
#         conn.send(msg.encode())
#         if msg == 'QUIT':
#             receive = conn.recv(1024)
#             print(receive.decode())
#             run = False
#         else:
#             receive = conn.recv(1024)
#             print(receive.decode())
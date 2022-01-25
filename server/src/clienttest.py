import socket
import ssl
import threading

HOST = "127.0.0.1"
PORT = 60002

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile="C:\\Users\\mciec\\Desktop\\Studia\\OD\\Project_OD\\server\\src\\cert.pem")
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
context.set_ciphers('AES256+ECDH:AES256+EDH')
conn = context.wrap_socket(client, server_hostname='127.0.0.1')


def receiveServerData():
    conn.connect(('127.0.0.1',60000))
    run = True
    while run:
        msg = input()
        conn.send(msg.encode())
        if msg == 'QUIT':
            receive = conn.recv(1024)
            print(receive.decode())
            run = False
        else:
            receive = conn.recv(1024)
            print(receive.decode())


receiveThread = threading.Thread(target=receiveServerData)
receiveThread.start()
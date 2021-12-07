class User:
    def __init__(self, tcpConn, name, addr):
        self.tcpConn = tcpConn
        self.name = name
        self.tcpAddr = addr
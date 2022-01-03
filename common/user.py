class User:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
    
    def get_ip_address(self):
        return self.addr
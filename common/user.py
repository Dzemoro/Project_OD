class User:
    def __init__(self, conn, addr, calling : bool):
        self.conn = conn
        self.addr = addr
        self.calling = calling
    
    def get_ip_address(self):
        return self.addr
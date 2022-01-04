from sys import path
from typing import List
if '' not in path:
    path.append('')
import os
from server import Server

if __name__ == "__main__":
    server = Server('127.0.0.1', 60000)
    server.run()
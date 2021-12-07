import os
from server.src.server import Server

file_problem = False
ip_regex = "^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.txt')
      
try:
    file = open(filename, "r")
    content = file.read().splitlines()
    ip = content[0]
    tcp_port = content[1]
    file.close()
    if(ip.lower() != 'auto' and ip != '' and not re.search(ip_regex, ip)):
        raise ValueError('Wrong IP address')
    if(tcp_port.lower() != 'auto' and tcp_port != '' and (int(tcp_port) > 65535 or int(tcp_port) < 1)):
        raise ValueError('Wrong port')
except ValueError as er:
    print("Config error: "+str(er)+"\nProper config.txt file:\n   1st line is server IP (you may use 'auto' or '')\n   2nd line is server port to listen on (you may use 'auto' or '')")
    input()
    file_problem = True
except:
    print("Missing proper config.txt file:\n   1st line is server IP (you may use 'auto' or '')\n   2nd line is server port to listen on (you may use 'auto' or '')")
    input()
    file_problem = True

if(not file_problem):
    server = Server(ip, tcp_port)
# By Olivia Toth 250965299

import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 3357
server_info = ('127.0.0.1', 3357)

print("Attempting to contact:", server_info[0] + ":" + str(server_info[1]))
# Create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Client connects to the server
s.connect((TCP_IP, TCP_PORT))

try:
    request = input("Enter request: ")
    print ("Connection to server established, sending request....")
    # Send request from user
    s.sendall(request.encode())
    # Get response from server
    data = s.recv(1024)
    print("Response from server:")
    print(data.decode())
finally:
    # Client closes connection
    s.close()

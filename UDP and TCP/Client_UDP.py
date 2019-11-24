# By Olivia Toth 250965299

import socket
import sys

# Create a UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

TCP_IP = '127.0.0.1'
TCP_PORT = 3357
server_info = ('127.0.0.1', 3357)

try:
    request = input("Enter request: ")
    print ("Sending request....")
    # Send request from user
    s.sendto(request.encode(), (TCP_IP, TCP_PORT))
    # Get response from server
    data, server = s.recvfrom(1024)
    print("Response from server:")
    print(data.decode())
finally:
    # Client closes connection
    s.close()

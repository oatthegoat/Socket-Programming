# By Olivia Toth 250965299

import socket
import sys
from datetime import datetime

TCP_IP = '127.0.0.1'
TCP_PORT = 3357
server_info = ('127.0.0.1', 3357)

# Create UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind socket to the port
s.bind((TCP_IP, TCP_PORT))

print("Server address:", server_info[0] + ":" + str(server_info[1]))
print("Waiting to receive request...")
while True:
    # Get request
    data, addr = s.recvfrom(1024)
    print("Client address:", addr[0] + ":" + str(addr[1]))
    if data.decode() == "What is the current date and time?":
        print("Sending response to client request...")
        # Send date/time response if user request was valid
        date_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        string = "{} {}".format("Current Date and Time -", date_time)
        s.sendto(string.encode(), addr)
    else:
        print("Sending response to client request...")
        # Send error response if user request was invalid
        string = "Error: Invalid Request"
        s.sendto(string.encode(), addr)

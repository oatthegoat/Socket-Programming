#By Olivia Toth 250965299

import binascii
import socket
import struct
import sys
import hashlib
import random
import time

#Provided function to enable network delay
def Network_Delay():
    if True and random.choice([0,1,0]) == 1: #Set to False to disable Network Delay. Default is 33% packets are delayed
        time.sleep(.01)
        print("Packet Delayed")
    else:
        print("Packet Sent")

#Provided function to enable network loss
def Network_Loss():
    if True and random.choice([0,1,1,0]) == 1: #Set to False to disable Network Loss. Default is 50% packets are lost
        print("Packet Lost\n")
        return(1)
    else:
        return(0)

#Provided function to corrupt packet data
def Packet_Checksum_Corrupter(packetdata):
    if True and random.choice([0,1,0,1]) == 1: #Set to False to disable Packet Corruption. Default is 50% packets are corrupt
        return(b"Corrupt!")
    else:
        return(packetdata)

#My function to create the checksum
def Create_Checksum(ack_number, seq_number, data):
    server_values = (ack_number, seq_number, data)
    UDP_Data = struct.Struct('I I 8s')
    server_packed_data = UDP_Data.pack(*server_values)
    server_chksum =  bytes(hashlib.md5(server_packed_data).hexdigest(), encoding="UTF-8")
    return server_chksum

#My function to build the UDP packet and send it to the client
def Build_And_Send(ack_number, seq_number, data, chksum):
    #Client port
    UDP_SEND_PORT = 4457

    #Uncomment the next line to enable packet data corruption
    #data = Packet_Checksum_Corrupter(data)

    #Build the UDP Packet
    values = (ack_number, seq_number, data, chksum)
    UDP_Packet_Data = struct.Struct('I I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)

    #Uncomment the next line to enable network delay
    #Network_Delay()

    #Open a socket to send messages and send the UDP Packet
    send = 0
    #Uncomment the next line to enable network loss
    #send = Network_Loss()
    if send == 0:
        sock.sendto(UDP_Packet, (UDP_IP, UDP_SEND_PORT))
        print ("Packet:", values, "sent to client\n")

#My function to flip the sequence number
def Flip_Expected_Sequence_Number(seq_number):
    if seq_number == 0:
        return 1
    else:
        return 0

UDP_IP = "127.0.0.1"
UDP_RCV_PORT = 3357
unpacker = struct.Struct('I I 8s 32s')

#Open a socket to receive messages
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_RCV_PORT))

expected_sequence_number = 0

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) #Buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)
    print("Received from:", addr)
    print("Received message:", UDP_Packet)

    #Create the Checksum for comparison
    chksum = Create_Checksum(UDP_Packet[0], UDP_Packet[1], UDP_Packet[2])

    send_data = b""

    #Compare Checksums to test for corrupt data
    if UDP_Packet[3] == chksum:
        print("CheckSums Match, Packet OK")

        #Detect duplicate packet
        if UDP_Packet[1] == expected_sequence_number:
            #Checksums and sequence number match so everything is fine
            print("Packet contained expected sequence number - not a duplicate packet")
            #Send a packet back to the client and flip the expected sequence number for the next incoming packet
            returned_chksum = Create_Checksum(1, expected_sequence_number, send_data)
            Build_And_Send(1, expected_sequence_number, send_data, returned_chksum)
            expected_sequence_number = Flip_Expected_Sequence_Number(UDP_Packet[1])
        else:
            #Checksums match but the sequence number doesn't so this is a duplicate packet
            print("Packet contained unexpected sequence number - duplicate packet")
            #Send a packet back to the client with the sequence number as is
            returned_chksum = Create_Checksum(1, UDP_Packet[1], send_data)
            Build_And_Send(1, UDP_Packet[1], send_data, returned_chksum)
    else:
        print("Checksums Do Not Match, Packet Corrupt")
        #Checksums don't match so the packet that was sent to the server was corrupt
        expected_sequence_number = Flip_Expected_Sequence_Number(UDP_Packet[1])
        #Send a packet back to the client with the sequence number flipped so the client knows to resend the packet which arrived corrupted
        returned_chksum = Create_Checksum(1, expected_sequence_number, send_data)
        Build_And_Send(1, expected_sequence_number, send_data, returned_chksum)

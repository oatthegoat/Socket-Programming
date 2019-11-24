#By Olivia Toth 250965299

import binascii
import socket
import struct
import sys
import hashlib

#My function to create the checksum
def Create_Checksum(ack_number, seq_number, data):
    values = (ack_number, seq_number, data)
    UDP_Data = struct.Struct('I I 8s')
    packed_data = UDP_Data.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    return chksum

#My function to flip the sequence number
def Flip_Sequence_Number(seq_number):
    if seq_number == 0:
        return 1
    else:
        return 0

UDP_IP = "127.0.0.1"
UDP_SEND_PORT = 3357

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_SEND_PORT, "\n")

unpacker = struct.Struct('I I 8s 32s')
seq = 0
data = [b'NCC-1701', b'NCC-1422', b'NCC-1017']

for i in data:
    resend = True
    while resend:
        #Create the Checksum
        client_chksum = Create_Checksum(0, seq, i)

        #Build the UDP Packet
        values = (0, seq, i, client_chksum)
        UDP_Packet_Data = struct.Struct('I I 8s 32s')
        UDP_Packet = UDP_Packet_Data.pack(*values)

        #Open a socket to send messages and send the UDP Packet
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(UDP_Packet, (UDP_IP, UDP_SEND_PORT))
        print ("Packet:", values, "sent to server, waiting for acknowledgement")

        #Close the send socket here so it doesn't confuse my timer
        sock.close()

        #Open a socket to receive messages
        UDP_RCV_PORT = 4457
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_RCV_PORT))

        #Set a timer for 9 milliseconds
        sock.settimeout(0.009)

        try:
            #Receive Data
            data_from_server, addr = sock.recvfrom(1024)
            server_packet = unpacker.unpack(data_from_server)
            print("Received from:", addr)
            print("Received message:", server_packet)

            #Create the Checksum for comparison
            server_chksum = Create_Checksum(server_packet[0], server_packet[1], server_packet[2])
            #Compare Checksums to test for corrupt data
            if server_chksum == server_packet[3]:
                if seq == server_packet[1]:
                    #The packet sent by the client was not lost or corrupt
                    print("CheckSums Match, Packet OK\n")
                    seq = Flip_Sequence_Number(seq)
                    resend = False
                else:
                    #The packet sent by the client was lost or corrupt
                    print("Packet contained unexpected sequence number - packet sent to server was lost or corrupt")
                    resend = True
                    print ("Resending Packet...\n")

            else:
                #Checksums don't match so the packet that was sent to the client was corrupt
                print ("CheckSums Do Not Match, Packet Corrupt")
                resend = True
                print ("Resending Packet...\n")

        except socket.timeout:
            #Timer expired
            print ("Timer Expired")
            resend = True
            print ("Resending Packet...\n")

#Close the receive socket here
sock.close()

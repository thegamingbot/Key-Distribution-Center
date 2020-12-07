r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
import os
import platform
import sqlite3
import subprocess
import sys
from pickle import loads
from socket import *
import time

from cryptography.fernet import Fernet

from constants import IPsAndPorts


# Open the file in the default application
from .verify import *


def recvTicket(csoc):
    ticket = loads(csoc.recv(2048))
    conn = sqlite3.connect('../sqlite.db')
    server = conn.execute('''
        SELECT USERNAME, PASSWORD, ENCRYPT_KEY
        FROM SERVER WHERE USERNAME='fileTransfer';''').fetchone()
    serverKey = Fernet(server[2]).decrypt(server[1])
    if Fernet(serverKey).decrypt(ticket[1]) == ticket[0]:
        csoc.send(bytes("y", "utf-8"))
    else:
        csoc.send(bytes("n", "utf-8"))
        csoc.close()
        while True:
            x = 1


def openFile(fileName):
    # If the platform is Windows
    if platform.system() == 'Windows':
        # Start the file
        os.startfile(fileName)
    # If the platform is Linux
    else:
        # Call the file
        subprocess.call(('xdg-open', fileName))
    # Exit the program
    sys.exit()


# Main driver function for the server
def fileIOServer():
    # Get the host name
    host = ""
    # Get the port number
    port = IPsAndPorts["File Transfer Server"][1]

    # Create the server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Bind the server to the host and port
    serverSocket.bind((host, port))

    # Listen for connection requests
    serverSocket.listen(10)
    # Accept the connection request from a client
    clientSocket, clientAddress = serverSocket.accept()
    recvTicket(clientSocket)
    # Expected sequence number
    expSeqN = 1

    # Receive the file name
    fileName = clientSocket.recv(1024).decode("utf-8")

    # Open the file
    fp = open(fileName, "wb")
    # Initialize is EOF as false
    isEOF = False
    # Get the time of the last packet time
    lastPacketTime = time.time()

    # Run an infinite loop
    while True:
        # If eof is reached
        if isEOF:
            # Break out of the loop
            break
        # Try
        try:
            # Receive the file file packet
            packet = clientSocket.recv(4096)
            # Parse and verify the received packet
            recvPacket, isCorrupt = parseAndVerify(packet)
            # If the received data is not corrupted
            if not isCorrupt:
                # If the received sequence number is the same as expected sequence number
                if recvPacket[0] == expSeqN:
                    # If the file data exists
                    if recvPacket[1]:
                        # Write the data
                        fp.write(recvPacket[1])
                    # If file data does not exits
                    else:
                        # EOF is reached
                        isEOF = True
                    # Increment the expected sequence number
                    expSeqN = expSeqN + 1
                    # Make the acknowledgement packet
                    sendPacket = makeACK(expSeqN)
                    # Send the acknowledgement packet
                    clientSocket.send(sendPacket)
                # If sequence numbers is mismatched
                else:
                    # Make the acknowledgement packet
                    sendPacket = makeACK(expSeqN)
                    # Send the acknowledgement packet
                    clientSocket.send(sendPacket)
        # If the file was not received
        except Exception as e:
            # Print the error
            exceptions = [e]
            break
    # Close the file
    fp.close()
    # Open the file
    openFile(fileName)


if __name__ == '__main__':
    fileIOServer()

r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
import os
import sqlite3
import subprocess
import sys
from pickle import loads
from socket import *
from threading import Thread

from cryptography.fernet import Fernet

from constants import IPsAndPorts

# Open the file in the default application
from verify import *


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


def runner(clientSocket):
    recvTicket(clientSocket)
    # Expected sequence number
    expSeqN = 1
    # Receive the file name
    fileName = clientSocket.recv(1024).decode("utf-8")
    # Open the file
    fp = open(fileName, "wb")
    # Initialize is EOF as false
    fp.write(clientSocket.recv(20480))
    # Close the file
    fp.close()
    print("File received: " + fileName)
    # openFile(fileName)


# def openFile(fileName):
#     # If the platform is Windows
#     if sys.platform.system() == 'Windows':
#         # Start the file
#         os.startfile(fileName)
#     # If the platform is Linux
#     else:
#         # Call the file
#         subprocess.call(('xdg-open', fileName))
#     # Exit the program
#     sys.exit()


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
    clients = []
    # Listen for connection requests
    serverSocket.listen()
    # Accept the connection request from a client
    while True:
        clientSocket, clientAddress = serverSocket.accept()
        clients.append(clientSocket)
        Thread(target=runner, args=(clients[-1], )).start()


if __name__ == '__main__':
    fileIOServer()

import socket
import sys
from threading import Thread


def send():
    while True:
        msg = input(f'{my_username} --> ')
        if msg == "quit":
            sys.exit()
        msg = msg.encode('utf-8')
        msg_len = f"{len(msg):<{MAX}}".encode('utf-8')
        client_socket.send(msg_len + msg)


def receive():
    while True:
        # Receive our "header" containing username length, it's size is defined and constant
        user_len = client_socket.recv(MAX)
        if not len(user_len):
            print('Connection closed by the server')
            sys.exit()
        # Convert header to int value
        username_length = int(user_len.decode('utf-8').strip())
        # Receive and decode username
        user = client_socket.recv(username_length).decode('utf-8')
        # Now do the same for message
        message_len = client_socket.recv(MAX)
        message_length = int(message_len.decode('utf-8').strip())
        message = client_socket.recv(message_length).decode('utf-8')
        # Print message
        print(f'{user} --> {message}')


MAX = 1024
IP = "127.0.0.1"
PORT = 9001
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# Prepare username and header and send them
username = my_username.encode('utf-8')
username_len = f"{len(username):<{MAX}}".encode('utf-8')
client_socket.send(username_len + username)

sendThread = Thread(target=send)
sendThread.start()
recvThread = Thread(target=receive)
recvThread.start()

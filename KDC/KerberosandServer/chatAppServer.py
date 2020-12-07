import socket
import sqlite3
from pickle import loads
from threading import Thread

from cryptography.fernet import Fernet

from constants import IPsAndPorts

MAX = 1024
IP = ""
PORT = IPsAndPorts["Chat App Server"][1]
sockets_list = []
clients = {}


# Handles message receiving
def receive_message(client):
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_len = client.recv(MAX)
        if not len(message_len):
            return False
        # Convert header to int value
        message_length = int(message_len.decode('utf-8'))
        # Return an object of message header and message data
        return {'header': message_len, 'data': client.recv(message_length)}
    except Exception as err:
        input(err)
        return False


def recvMessage(current_socket):
    while True:
        # Receive message
        message = receive_message(current_socket)
        # If False, client disconnected, cleanup
        if message is False:
            print('Closed connection from: {}'.format(clients[current_socket]['data'].decode('utf-8')))
            # Remove from list for socket.socket()
            sockets_list.remove(current_socket)
            # Remove from our list of users
            del clients[current_socket]
            return

        # Get user by notified socket, so we will know who sent the message
        user = clients[current_socket]
        print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
        # Iterate over connected clients and broadcast message
        for csoc in clients:
            # Send user and message (both with their headers)
            csoc.send(user['header'])
            csoc.send(user['data'])
            csoc.send(message['header'])
            csoc.send(message['data'])


def recvTicket(csoc):
    ticket = loads(csoc.recv(2048))
    conn = sqlite3.connect('../sqlite.db')
    server = conn.execute('''
        SELECT USERNAME, PASSWORD, ENCRYPT_KEY
        FROM SERVER WHERE USERNAME='chatApp';''').fetchone()
    serverKey = Fernet(server[2]).decrypt(server[1])
    if Fernet(serverKey).decrypt(ticket[1]) == ticket[0]:
        csoc.send(bytes("y", "utf-8"))
    else:
        csoc.send(bytes("n", "utf-8"))
        csoc.close()
        while True:
            x = 1


def connectionHandler(ssoc):
    while True:
        # Accept new connection
        csoc, client_address = ssoc.accept()
        recvTicket(csoc)
        user = receive_message(csoc)
        # If False - client disconnected before he sent his name
        if user is False:
            continue
        # Add accepted socket to select.select() list
        sockets_list.append(csoc)
        # Also save username and username header
        clients[csoc] = user
        print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                        user['data'].decode('utf-8')))
        Thread(target=recvMessage, args=(csoc,)).start()


def server_run():
    # Create a socket
    ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind
    ssoc.bind((IP, PORT))
    # Listen
    ssoc.listen()
    # List of connected clients - socket as a key, user header and name as data
    print(f'Listening for connections on {IP}:{PORT}...')
    connectionHandler(ssoc)


if __name__ == '__main__':
    server_run()

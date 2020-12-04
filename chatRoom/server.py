import socket
from threading import Thread

MAX = 1024
IP = "127.0.0.1"
PORT = 9001


# Handles message receiving
def receive_message(client):
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_len = client.recv(MAX)
        if not len(message_len):
            return False
        # Convert header to int value
        message_length = int(message_len.decode('utf-8').strip())
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
            # But don't sent it to sender
            if csoc != current_socket:
                # Send user and message (both with their headers)
                csoc.send(user['header'] + user['data'] + message['header'] + message['data'])


def connectionHandler():
    while True:
        # Accept new connection
        csoc, client_address = ssoc.accept()
        # Client should send his name right away, receive it
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
        Thread(target=recvMessage, args=(csoc, )).start()


# Create a socket
ssoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind
ssoc.bind((IP, PORT))
# Listen
ssoc.listen()
# List of sockets for select.select()
sockets_list = [ssoc]
# List of connected clients - socket as a key, user header and name as data
clients = {}
print(f'Listening for connections on {IP}:{PORT}...')
connectionHandler()

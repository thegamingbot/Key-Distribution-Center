import socket
import sys
import errno

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

while True:

    # Wait for user to input a message

    message = input(f'{my_username} --> ')
    # If message is not empty - send it
    if message:
        message = message.encode('utf-8')
        message_len = f"{len(message):<{MAX}}".encode('utf-8')
        client_socket.send(message_len + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:
            # Receive our "header" containing username length, it's size is defined and constant
            username_len = client_socket.recv(MAX)
            if not len(username_len):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_len.decode('utf-8').strip())
            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
            # Now do the same for message
            message_len = client_socket.recv(MAX)
            message_length = int(message_len.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} --> {message}')

    except IOError as e:
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()

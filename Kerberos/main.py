import socket
import sqlite3
from cryptography.fernet import Fernet
from pickle import loads
from uuid import uuid4
from threading import *


def login(soc, username, password):
    conn = sqlite3.connect('./sqlite.db')
    users = conn.execute('''SELECT *
            FROM USER''')
    flag = False
    for _ in users:
        if username == _[0]:
            cipher = Fernet(_[2])
            if cipher.decrypt(_[1]).decode("utf-8") == password:
                flag = True
    if flag:
        soc.send(bytes("y", 'utf-8'))
    else:
        soc.send(bytes("n", 'utf-8'))


def register(soc, username, password):
    conn = sqlite3.connect('../sqlite.db')
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encryptedPassword = cipher.encrypt(bytes(password, "utf-8"))
    conn.execute('''INSERT INTO USER
                (USERNAME, PASSWORD, ENCRYPT_KEY) VALUES
                (?, ?, ?);''', (username, encryptedPassword, key))
    conn.commit()
    soc.send(bytes("y", 'utf-8'))


def authentication(soc):
    args = loads(soc.recv(1024))
    if args[2] == "login":
        login(soc, args[0], args[1])
    elif args[2] == "register":
        register(soc, args[0], args[1])


def authenticationServer():
    authServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9003
    authServer.bind((host, port))
    clients = []
    authServer.listen()
    while True:
        clients.append(authServer.accept())
        thread = Thread(target=authentication, args=(clients[-1][0],))
        thread.start()


if __name__ == "__main__":
    authThread = Thread(target=authenticationServer)
    authThread.start()

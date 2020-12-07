import base64
import socket
import sqlite3
from cryptography.fernet import Fernet
from pickle import loads, dumps
from threading import *
from constants import *

masterKey = Fernet.generate_key()


def login(soc, username, password):
    conn = sqlite3.connect('../sqlite.db')
    users = conn.execute('''SELECT *
            FROM USER''')
    flag = False
    TGT = []
    for _ in users:
        if username == _[0]:
            cipher = Fernet(_[2])
            if cipher.decrypt(_[1]).decode("utf-8") == password:
                sessionKey = Fernet.generate_key()
                userKey = password * 5
                TGT.append(Fernet(masterKey).encrypt(sessionKey))
                TGT.append(Fernet(base64.urlsafe_b64encode(bytes(userKey[:32], "utf-8"))).
                           encrypt(sessionKey))
                flag = True
    if flag:
        soc.send(bytes("t", 'utf-8'))
        soc.send(dumps(TGT))
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
    host = ""
    port = ASPort
    authServer.bind((host, port))
    clients = []
    authServer.listen()
    while True:
        clients.append(authServer.accept())
        thread = Thread(target=authentication, args=(clients[-1][0],))
        thread.start()


def ticketGeneration(sessionKey, server):
    decryptedServer = Fernet(sessionKey).decrypt(server).decode("utf-8")
    conn = sqlite3.connect('../sqlite.db')
    if decryptedServer == "Chat App Server":
        server = conn.execute('''
            SELECT USERNAME, PASSWORD, ENCRYPT_KEY
            FROM SERVER WHERE USERNAME='chatApp';''').fetchone()
        serverKey = Fernet(server[2]).decrypt(server[1])
        newSessionKey = Fernet.generate_key()
        ticket = [
            Fernet(serverKey).encrypt(newSessionKey),
            Fernet(sessionKey).encrypt(newSessionKey),
            IPsAndPorts[decryptedServer][0],
            IPsAndPorts[decryptedServer][1]
        ]
        return [ticket, decryptedServer]
    elif decryptedServer == "Quiz Server":
        server = conn.execute('''
            SELECT USERNAME, PASSWORD, ENCRYPT_KEY
            FROM SERVER WHERE USERNAME='quiz';''').fetchone()
        serverKey = Fernet(server[2]).decrypt(server[1])
        newSessionKey = Fernet.generate_key()
        ticket = [
            Fernet(serverKey).encrypt(newSessionKey),
            Fernet(sessionKey).encrypt(newSessionKey),
            IPsAndPorts[decryptedServer][0],
            IPsAndPorts[decryptedServer][1]
        ]
        return [ticket, decryptedServer]
    elif decryptedServer == "File Transfer Server":
        server = conn.execute('''
            SELECT USERNAME, PASSWORD, ENCRYPT_KEY
            FROM SERVER WHERE USERNAME='fileTransfer';''').fetchone()
        serverKey = Fernet(server[2]).decrypt(server[1])
        newSessionKey = Fernet.generate_key()
        ticket = [
            Fernet(serverKey).encrypt(newSessionKey),
            Fernet(sessionKey).encrypt(newSessionKey),
            IPsAndPorts[decryptedServer][0],
            IPsAndPorts[decryptedServer][1]
        ]
        return [ticket, decryptedServer]
    else:
        return None


def ticketAuth(soc):
    inpList = loads(soc.recv(2048))
    if Fernet(masterKey).decrypt(inpList[1]) == inpList[0]:
        ticket = ticketGeneration(inpList[0], inpList[2])
        if ticket[0] is None:
            soc.send(bytes("n", "utf-8"))
        else:
            soc.send(bytes("y", "utf-8"))
            soc.send(dumps(ticket[0]))

    else:
        soc.send(bytes("n", "utf-8"))


def ticketGeneratingServer():
    TGSServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port = TGSPort
    TGSServer.bind((host, port))
    clients = []
    TGSServer.listen()
    while True:
        clients.append(TGSServer.accept())
        thread = Thread(target=ticketAuth, args=(clients[-1][0],))
        thread.start()


if __name__ == "__main__":
    authThread = Thread(target=authenticationServer)
    authThread.start()
    TGSThread = Thread(target=ticketGeneratingServer)
    TGSThread.start()

import socket
import sqlite3
from cryptography.fernet import Fernet


def login(username, password):
    conn = sqlite3.connect('sqlite.db')
    users = conn.execute('''SELECT *
            FROM USER''')
    flag = False
    for _ in users:
        if username == _[0]:
            cipher = Fernet(_[2])
            if cipher.decrypt(_[1]).decode("utf-8") == password:
                flag = True
    if flag:
        client.send(bytes("yes", 'utf-8'))
    else:
        client.send(bytes("no", 'utf-8'))


def register(username, password):
    conn = sqlite3.connect('sqlite.db')
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encryptedPassword = cipher.encrypt(bytes(password, "utf-8"))
    conn.execute('''INSERT INTO USER
                (USERNAME, PASSWORD, ENCRYPT_KEY) VALUES
                (?, ?, ?);''', (username, encryptedPassword, key))
    conn.commit()
    client.send(bytes("yes", 'utf-8'))


if __name__ == "__main__":
    kerberos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9001
    kerberos.bind((host, port))
    kerberos.listen()
    client, addr = kerberos.accept()
    function = client.recv(128).decode("utf-8")
    username = client.recv(128).decode("utf-8")
    password = client.recv(128).decode("utf-8")
    if function == "login":
        login(username, password)
    elif function == "register":
        register(username, password)

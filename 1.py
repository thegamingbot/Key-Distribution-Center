import sqlite3
from cryptography.fernet import Fernet
import secrets


if __name__ == '__main__':
    conn = sqlite3.connect('sqlite.db')
    conn.execute('''
    CREATE TABLE USER(
    USERNAME    TEXT    NOT NULL    PRIMARY KEY,
    PASSWORD    TEXT    NOT NULL,
    ENCRYPT_KEY TEXT    NOT NULL
    );''')
    conn.execute('''
    CREATE TABLE SERVER(
    USERNAME    TEXT    NOT NULL    PRIMARY KEY,
    PASSWORD    TEXT    NOT NULL,
    ENCRYPT_KEY TEXT    NOT NULL
    );''')
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encryptedPassword = cipher.encrypt(Fernet.generate_key())
    conn.execute('''INSERT INTO SERVER
                (USERNAME, PASSWORD, ENCRYPT_KEY) VALUES
                (?, ?, ?);''', ("chatApp", encryptedPassword, key))
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encryptedPassword = cipher.encrypt(Fernet.generate_key())
    conn.execute('''INSERT INTO SERVER
                (USERNAME, PASSWORD, ENCRYPT_KEY) VALUES
                (?, ?, ?);''', ("fileTransfer", encryptedPassword, key))
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encryptedPassword = cipher.encrypt(Fernet.generate_key())
    conn.execute('''INSERT INTO SERVER
                (USERNAME, PASSWORD, ENCRYPT_KEY) VALUES
                (?, ?, ?);''', ("quiz", encryptedPassword, key))
    conn.commit()

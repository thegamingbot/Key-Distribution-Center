import sqlite3
from pickle import dumps, loads
from random import shuffle
from socket import *
from threading import Thread
from time import time

from cryptography.fernet import Fernet
from constants import IPsAndPorts


def initQuestions():
    return [{
        'question': "How are the players called in Valorant?",
        'choices': ["Players", "Soldiers", "Agents", "Merchs"],
        'answer': "Agents"
    }, {
        'question': "Which Valorant gun has the highest magazine capacity?",
        'choices': ["Frenzy", "Ghost", "Shorty", "Sheriff"],
        'answer': "Ghost"
    }, {
        'question': "Whose ultimate ability lasts the longest?",
        'choices': ["Omen", "Jett", "Brimstone", "Phoenix"],
        'answer': "Omen"
    }, {
        'question': "Which class is Renya?",
        'choices': ["Initiator", "Sentinel", "Duelist", "Controller"],
        'answer': "Duelist"
    }, {
        'question': "How many credits does the Operator cost?",
        'choices': ["4500", "3600", "3200", "2900"],
        'answer': "4500"
    }, {
        'question': "Which rifle has the lowest damage value to the head?",
        'choices': ["Vandal", "Guardian", "Phantom", "Bulldog"],
        'answer': "Bulldog"
    }, {
        'question': "How much range does Sova’s Ultimate have?",
        'choices': ["Infinite", "50m", "24m", "4m"],
        'answer': "Infinite"
    }, {
        'question': "What does Viper say when she uses her Ultimate ability?",
        'choices': ["I'll leave you breathless", "Welcome to my zone", "Don't get in my way", "You destroyed my home"],
        'answer': "Don't get in my way"
    }]


clients = []
questions = initQuestions()


def gameLoop(data):
    data["name"] = data["client"].recv(100).decode("utf-8")
    clients.append(data)
    answers = []
    ques = []
    print(data["name"] + " has joined the quiz")
    shuffle(questions)
    for i in range(5):
        shuffle(questions[i]["choices"])
        ques.append([questions[i]["question"], questions[i]["choices"]])
        answers.append(questions[i]["answer"])
    start = time()
    data["client"].send(dumps(ques))
    output = loads(data["client"].recv(2048))
    end = time()
    out = [0, end - start]
    for i in range(5):
        if answers[i] == output[i]:
            out[0] += 1
    data["client"].send(dumps(out))
    data["client"].close()


def recvTicket(csoc):
    ticket = loads(csoc.recv(2048))
    conn = sqlite3.connect('../sqlite.db')
    server = conn.execute('''
        SELECT USERNAME, PASSWORD, ENCRYPT_KEY
        FROM SERVER WHERE USERNAME='quiz';''').fetchone()
    serverKey = Fernet(server[2]).decrypt(server[1])
    if Fernet(serverKey).decrypt(ticket[1]) == ticket[0]:
        csoc.send(bytes("y", "utf-8"))
    else:
        csoc.send(bytes("n", "utf-8"))
        csoc.close()
        while True:
            x = 1


def quizServer():
    server = socket(AF_INET, SOCK_STREAM)
    host = ""
    port = IPsAndPorts["Quiz Server"][1]
    server.bind((host, port))
    server.listen()
    while True:
        client, addr = server.accept()
        recvTicket(client)
        clients.append({"client": client, "addr": addr, "name": "", "time": 1000.0})
        clientThread = Thread(target=gameLoop, args=(clients[-1],))
        clientThread.start()


if __name__ == '__main__':
    quizServer()

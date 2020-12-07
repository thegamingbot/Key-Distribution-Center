import sys
import socket
from pickle import dumps
from time import *
from PyQt5 import QtCore, QtWidgets
import re

from cryptography.fernet import Fernet

MAX = 1024


class ChatRoom(QtWidgets.QWidget):
    """Basic chat window.
    """
    def __init__(self, name, ticket):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ticket[2]
        self.port = ticket[3]
        self.sessionKey = Fernet(ticket[4]).decrypt(ticket[1])
        self.ticket = ticket[0]
        print(self.host, self.port)
        self.name = name
        self.worker = workerThread(self.client_socket)
        self.widget = QtWidgets.QWidget(self)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()

        self.messagesBox = QtWidgets.QTextEdit(self.widget)
        self.send = QtWidgets.QPushButton(self.widget)
        self.textBox = QtWidgets.QTextEdit(self.widget)
        self.setupUI()

    def setupUI(self):
        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #FF0000;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #800000;
                border-style: inset;
            }
            """
        )

        self.messagesBox.setMinimumSize(QtCore.QSize(0, 40))
        self.messagesBox.setPlaceholderText("Messages")
        self.messagesBox.setReadOnly(True)
        self.messagesBox.setStyleSheet("QTextEdit {\n"
                                       "color: red;\n"
                                       "font: 15pt \"Verdana\";\n"
                                       "border: 1px solid white;\n"
                                       "border-bottom-color: white;\n"
                                       "border-radius: 10px;\n"
                                       "padding: 0 8px;\n"
                                       "background: rgb(0,0,0);\n"
                                       "selection-background-color: darkgray;\n"
                                       "}")
        self.messagesBox.setFocus()
        self.verticalLayout_1.addWidget(self.messagesBox)

        self.textBox.setMinimumSize(QtCore.QSize(0, 40))
        self.textBox.setPlaceholderText("Enter your message")
        self.textBox.setStyleSheet("QTextEdit {\n"
                                   "color: red;\n"
                                   "font: 15pt \"Verdana\";\n"
                                   "border: 1px solid white;\n"
                                   "border-bottom-color: white;\n"
                                   "border-radius: 10px;\n"
                                   "padding: 0 8px;\n"
                                   "background: rgb(0,0,0);\n"
                                   "selection-background-color: darkgray;\n"
                                   "}")
        self.textBox.setFocus()
        self.textBox.ensureCursorVisible()

        self.send.setMinimumSize(QtCore.QSize(0, 60))
        self.send.setAutoFillBackground(False)
        self.send.setText("Send")
        self.send.setStyleSheet("color: rgb(255, 255, 255);\n"
                                "font: 17pt \"Verdana\";\n"
                                "border: 2px solid red;\n"
                                "padding: 5px;\n"
                                "border-radius: 3px;\n"
                                "opacity: 200;\n"
                                "")
        self.send.setAutoDefault(True)
        self.send.clicked.connect(self.send_msg)
        self.horizontalLayout_1.addWidget(self.textBox)
        self.horizontalLayout_1.addWidget(self.send)
        self.verticalLayout_3.addLayout(self.verticalLayout_1, 5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_1, 1)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: rgb(0, 0, 0);}")
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.sendTicket()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Chat Room", "Chat Room - " + self.name))

    def sendTicket(self):
        self.setEnabled(False)
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(dumps([self.sessionKey, self.ticket]))
        verify = self.client_socket.recv(1).decode("utf-8")
        if verify == "n":
            sys.exit()
        else:
            self.setEnabled(True)
            self.client_run()

    def send_msg(self):
        msg = self.textBox.toPlainText()
        if re.match(r'^\s*$', msg):
            return
        msg = msg.encode('utf-8')
        msg_len = f"{len(msg):<{MAX}}".encode('utf-8')
        self.textBox.setText("")
        self.client_socket.send(msg_len + msg)

    def receive(self, user, message):
        msg = self.messagesBox.toPlainText() + "\n" + str(ctime(time())) + "\n" + user + ' --> ' + message + "\n"
        self.messagesBox.setText(msg)
        self.messagesBox.verticalScrollBar().setValue(self.messagesBox.verticalScrollBar().maximum())

    def client_run(self):
        # Prepare username and header and send them
        username = self.name.encode('utf-8')
        username_len = f"{len(username):<{MAX}}".encode('utf-8')
        self.client_socket.send(username_len + username)
        self.worker.start()
        self.worker.updateMessage.connect(self.receive)


class workerThread(QtCore.QThread):
    updateMessage = QtCore.pyqtSignal(str, str)

    def __init__(self, client):
        super().__init__()
        self.client_socket = client

    def run(self):
        while True:
            # Receive our "header" containing username length, it's size is defined and constant
            user_len = self.client_socket.recv(MAX)
            if not len(user_len):
                sys.exit()
            # Convert header to int value
            username_length = int(user_len.decode('utf-8'))
            # Receive and decode username
            username = self.client_socket.recv(username_length).decode('utf-8')
            # Now do the same for message
            message_len = self.client_socket.recv(MAX)
            message_length = int(message_len.decode('utf-8'))
            message = self.client_socket.recv(message_length).decode('utf-8')
            self.updateMessage.emit(username, message)

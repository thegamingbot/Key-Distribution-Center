import sys
import socket
import time
from threading import Thread
from PyQt5 import QtCore, QtWidgets

MAX = 1024


class ChatRoom(QtWidgets.QWidget):
    """Basic chat window.
    """
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = "127.0.0.1"
        self.PORT = 9001
        self.name = name
        self.widget = QtWidgets.QWidget(self)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.widget)
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
        self.client_run()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Chat Room", "Chat Room - " + self.name))

    def send_msg(self):
        msg = self.textBox.toPlainText()
        # msg = input(f'{my_username} --> ')
        if msg == "quit":
            sys.exit()
        msg = msg.encode('utf-8')
        msg_len = f"{len(msg):<{MAX}}".encode('utf-8')
        self.client_socket.send(msg_len + msg)

    def receive(self):
        while True:
            # Receive our "header" containing username length, it's size is defined and constant
            user_len = self.client_socket.recv(MAX)
            if not len(user_len):
                sys.exit()
            # Convert header to int value
            username_length = int(user_len.decode('utf-8').strip())
            # Receive and decode username
            user = self.client_socket.recv(username_length).decode('utf-8')
            # Now do the same for message
            message_len = self.client_socket.recv(MAX)
            message_length = int(message_len.decode('utf-8').strip())
            message = self.client_socket.recv(message_length).decode('utf-8')
            msg = self.messagesBox.toPlainText() + '\n' + str(time.localtime(time.time())) + self.name + ' --> ' + message
            self.messagesBox.setText(msg)

    def client_run(self):
        self.client_socket.connect((self.IP, self.PORT))
        # Prepare username and header and send them
        username = self.name.encode('utf-8')
        username_len = f"{len(username):<{MAX}}".encode('utf-8')
        self.client_socket.send(username_len + username)

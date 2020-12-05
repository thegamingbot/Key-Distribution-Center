import socket
from pickle import loads

from PyQt5 import QtCore, QtWidgets


# def getTicket(username):
#     soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host = socket.gethostname()
#     port = 9003
#     soc.connect((host, port))
#     soc.send(username)
#     ticket = loads(soc.recv(2048))


class MainWindow(QtWidgets.QWidget):

    def __init__(self, username, sessionKey, TGT):
        QtWidgets.QWidget.__init__(self)
        self.username = username
        self.sessionKey = sessionKey
        self.TGT = TGT
        self.setWindowTitle(self.username + " - Client")
        layout = QtWidgets.QGridLayout()
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setText(str(self.sessionKey) + " " + str(self.TGT))
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        # getTicket(username)

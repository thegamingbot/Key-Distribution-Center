import sys
from socket import *
from pickle import loads, dumps

from PyQt5 import QtCore, QtWidgets
from cryptography.fernet import Fernet


class MainWindow(QtWidgets.QWidget):

    chatApp = QtCore.pyqtSignal(list)
    fileTransfer = QtCore.pyqtSignal(list)
    quiz = QtCore.pyqtSignal(list)

    def __init__(self, username, sessionKey, TGT):
        super().__init__()
        self.username = username
        self.sessionKey = sessionKey
        self.TGT = TGT
        self.widget = QtWidgets.QWidget(self)

        self.cb = QtWidgets.QComboBox(self.widget)
        self.line = QtWidgets.QFrame(self.widget)
        self.pushButton = QtWidgets.QPushButton(self.widget)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
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
        self.formLayout_2.setContentsMargins(50, 35, 59, -1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

        self.cb.addItems(["Chat App Server", "Quiz Server", "File Transfer Server"])
        self.cb.setStyleSheet("QComboBox {\n"
                              "color: red;\n"
                              "font: 15pt \"Verdana\";\n"
                              "border: None;\n"
                              "border-bottom-color: white;\n"
                              "border-radius: 10px;\n"
                              "padding: 0 8px;\n"
                              "background: rgb(0,0,0);\n"
                              "selection-background-color: darkgray;\n"
                              "}")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.cb)

        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())

        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "font: 17pt \"Verdana\";\n"
                                      "border: 2px solid red;\n"
                                      "padding: 5px;\n"
                                      "border-radius: 3px;\n"
                                      "opacity: 200;\n"
                                      "")
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.getTicket)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: rgb(0, 0, 0);}")

        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", self.username + " - Client"))
        self.pushButton.setText(_translate("Form", "Get Ticket"))

    def getTicket(self):
        self.cb.setEnabled(False)
        soc = socket(AF_INET, SOCK_STREAM)
        host = '34.67.114.239'
        port = 8050
        selection = self.cb.currentText()
        soc.connect((host, port))
        soc.send(dumps([self.sessionKey, self.TGT, Fernet(self.sessionKey)
                       .encrypt(bytes(selection, "utf-8"))]))
        if soc.recv(1).decode("utf-8") == "n":
            sys.exit()
        ticket = loads(soc.recv(2048))
        self.cb.setEnabled(True)
        ticket.append(self.sessionKey)
        # "Chat App Server", "Quiz Server", "File Transfer Server"
        if selection == "Chat App Server":
            self.chatApp.emit(ticket)
        elif selection == "Quiz Server":
            self.quiz.emit(ticket)
        else:
            self.fileTransfer.emit(ticket)

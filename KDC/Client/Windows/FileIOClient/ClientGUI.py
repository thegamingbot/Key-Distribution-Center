import os
import sys
import time
from pickle import dumps
from socket import *
from PyQt5 import QtWidgets, QtCore
from cryptography.fernet import Fernet

from .verify import *


class ClientUI(QtWidgets.QWidget):
    def __init__(self, ticket):
        super().__init__()
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.host = ticket[2]
        self.port = ticket[3]
        self.sessionKey = Fernet(ticket[4]).decrypt(ticket[1])
        self.ticket = ticket[0]
        self.group = QtWidgets.QButtonGroup()
        self.widget = QtWidgets.QWidget(self)
        self.filePath = ""

        self.label = QtWidgets.QLabel(self.widget)
        self.windowSpinBar = QtWidgets.QSpinBox(self.widget)
        self.pushButton_1 = QtWidgets.QPushButton(self.widget)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.line = QtWidgets.QFrame(self.widget)
        self.line_1 = QtWidgets.QFrame(self.widget)

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

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: rgb(0, 0, 0);}")

        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)

        self.formLayout_2.setContentsMargins(50, 35, 59, -1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(0, QtWidgets.QFormLayout.SpanningRole, spacerItem)

        self.label.setText("Sliding Window Size")
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setStyleSheet("QLabel {\n"
                                 "color: red;\n"
                                 "font: 18pt \"Verdana\";\n"
                                 "border: None;\n"
                                 "border-bottom-color: white;\n"
                                 "border-radius: 10px;\n"
                                 "padding: 0 8px;\n"
                                 "background: rgb(0,0,0);\n"
                                 "selection-background-color: darkgray;\n"
                                 "}")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label)

        self.windowSpinBar.setMinimumSize(QtCore.QSize(0, 40))
        self.windowSpinBar.setStyleSheet("QSpinBox {\n"
                                         "color: red;\n"
                                         "font: 30pt \"Verdana\";\n"
                                         "border: None;\n"
                                         "border-bottom-color: white;\n"
                                         "border-radius: 10px;\n"
                                         "padding: 0 8px;\n"
                                         "background: rgb(0,0,0);\n"
                                         "selection-background-color: darkgray;\n"
                                         "}")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.windowSpinBar)

        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(4, QtWidgets.QFormLayout.SpanningRole, spacerItem2)

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
        self.pushButton.clicked.connect(self.getFiles)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(6, QtWidgets.QFormLayout.SpanningRole, spacerItem3)

        self.line_1.setStyleSheet("border: 2px solid white;")
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.line_1)

        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(8, QtWidgets.QFormLayout.SpanningRole, spacerItem4)

        self.pushButton_1.setSizePolicy(sizePolicy)
        self.pushButton_1.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_1.setAutoFillBackground(False)
        self.pushButton_1.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font: 17pt \"Verdana\";\n"
                                        "border: 2px solid red;\n"
                                        "padding: 5px;\n"
                                        "border-radius: 3px;\n"
                                        "opacity: 200;\n"
                                        "")
        self.pushButton_1.setAutoDefault(True)
        self.pushButton_1.clicked.connect(self.sendFile)
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.pushButton_1)

        self.verticalLayout_3.addLayout(self.formLayout_2)

        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.retranslateUi("Select a file to send")
        self.sendTicket()

    def retranslateUi(self, btn):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Client"))
        self.pushButton.setText(_translate("MainWindow", btn))
        self.pushButton_1.setText(_translate("Send", "Send"))

    def sendTicket(self):
        self.setEnabled(False)
        self.clientSocket.connect((self.host, self.port))
        self.clientSocket.send(dumps([self.sessionKey, self.ticket]))
        verify = self.clientSocket.recv(1).decode("utf-8")
        if verify == "n":
            sys.exit()
        else:
            self.setEnabled(True)

    def getFiles(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.filePath = filenames[0]
            self.retranslateUi(os.path.basename(self.filePath))

    # A function to send the file to the receiver
    def sendFile(self):
        # Get the host name
        # Get the port number
        # Set the timeout to 2 seconds
        timeOut = 2
        # Create the client socket
        # Connect the socket to the appropriate host and port
        # Extract the file name from the file path and send it to the receiver
        self.clientSocket.send(bytes(os.path.basename(self.filePath), "utf-8"))
        # Open the file
        fp = open(self.filePath, 'rb')
        # Read the data
        data = fp.read()
        self.clientSocket.send(data)
        # Close the file
        fp.close()
        # Close the socket
        self.clientSocket.close()
        # Exit the application
        sys.exit(0)

import os
import sys
import time
from socket import *
from PyQt5 import QtWidgets, QtCore

from verify import *


class ClientUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.group = QtWidgets.QButtonGroup()
        self.widget = QtWidgets.QWidget(self)
        self.filePath = ""

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
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.windowSpinBar)

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

    def retranslateUi(self, btn):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Client"))
        self.pushButton.setText(_translate("MainWindow", btn))
        self.pushButton_1.setText(_translate("Send", "Send"))

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
        host = gethostname()
        # Get the port number
        port = 9001
        # Set the timeout to 2 seconds
        timeOut = 2
        # Create the client socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # Connect the socket to the appropriate host and port
        clientSocket.connect((host, port))
        # Extract the file name from the file path and send it to the receiver
        clientSocket.send(bytes(os.path.basename(self.filePath), "utf-8"))
        # Lower bound of the window
        base = 1
        # Next sequence number
        nextSeqN = 1
        # Window size extracted from the form
        windowSize = int(self.windowSpinBar.text())
        # Create the window list
        window = []
        # Open the file
        fp = open(self.filePath, 'rb')
        # Read the data
        data = fp.read(1024)
        # Set done as False
        done = False
        # Get the time of the last acknowledgement
        lastAckTime = time.time()
        # While there exists data in the window or not done
        while not done or window:
            # If there exists a space in the window and file is not done
            if (nextSeqN < base + windowSize) and not done:
                # Create the send packet with the data and sequence number
                sendPacket = makePkt(nextSeqN, data)
                # Send the created packet
                clientSocket.send(sendPacket)
                # Go the the next sequence number
                nextSeqN = nextSeqN + 1
                # Append the send packet to the window
                window.append(sendPacket)
                # Read the next data
                data = fp.read(1024)
                # If data is not available
                if not data:
                    # Done is true
                    done = True
            # Try receiving the acknowledgement
            try:
                # Receive the acknowledgement
                packet = clientSocket.recv(4096)
                # Parse and verify the received data
                recvPacket, isCorrupt = parseAndVerify(packet)
                # If the data is not corrupted
                if not isCorrupt:
                    # While receive packet greater than the lower bound and window is not empty
                    while recvPacket[0] > base and window:
                        # Update the time of latest acknowledgement
                        lastAckTime = time.time()
                        # Delete the first window
                        del window[0]
                        # Increment the base as the previous index is removed
                        base = base + 1
            # Exception if there is no acknowledgement
            except Exception as e:
                # Print the exception
                print(e)
                # If the time difference is greater than timeout
                if time.time() - lastAckTime > timeOut:
                    # Loop through the window
                    for i in window:
                        # Send each packet in the widow
                        clientSocket.send(i)
        # Close the file
        fp.close()
        # Close the socket
        clientSocket.close()
        # Exit the application
        sys.exit(0)

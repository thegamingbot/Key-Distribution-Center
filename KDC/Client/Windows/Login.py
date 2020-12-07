# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import base64

from PyQt5 import QtCore, QtWidgets
from cryptography.fernet import Fernet
import socket
from pickle import dumps, loads

from .customized import PasswordEdit


def auth(args):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8040
    soc.connect((host, port))
    soc.send(dumps(args))
    verify = soc.recv(1).decode('utf-8')
    if verify == "t":
        return loads(soc.recv(2048))
    return verify


class Login(QtWidgets.QWidget):
    """Basic login form.
    """
    switch_window = QtCore.pyqtSignal(str, bytes, bytes)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = QtWidgets.QWidget(self)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line = QtWidgets.QFrame(self.widget)
        self.lineEdit_2 = PasswordEdit(self.widget)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label = QtWidgets.QLabel(self.widget)

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

        self.label.setMinimumSize(QtCore.QSize(100, 150))
        self.label.setMaximumSize(QtCore.QSize(150, 150))
        self.label.setStyleSheet("image: url(icon/rocket_48x48.png);")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)

        self.formLayout_2.setContentsMargins(50, 35, 59, -1)

        self.label_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                   "font: 15pt \"Verdana\";")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setPlaceholderText("Enter your username")
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "color: red;\n"
                                    "font: 15pt \"Verdana\";\n"
                                    "border: None;\n"
                                    "border-bottom-color: white;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 0 8px;\n"
                                    "background: rgb(0,0,0);\n"
                                    "selection-background-color: darkgray;\n"
                                    "}")
        self.lineEdit.setFocus()
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setPlaceholderText("Enter your password")
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
                                      "color: red;\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: white;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: rgb(0,0,0);\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_2.setStyleSheet("border: 2px solid white;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.line_2)

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
        self.pushButton.clicked.connect(self.login)
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_2.setStyleSheet("color: rgb(255, 255, 244);\n"
                                        "font: 17pt \"Verdana\";\n"
                                        "border: 2px solid red;\n"
                                        "padding: 5px;\n"
                                        "border-radius: 3px;\n"
                                        "opacity: 200;\n"
                                        "")
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.clicked.connect(self.register)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(6, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.verticalLayout_3.addLayout(self.formLayout_2)

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
        self.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\"./Resources/icons/user_32x32.png\"/></p></body></html>"))
        self.label_3.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\"./Resources/icons/lock_32x32.png\"/></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Sign In"))
        self.pushButton_2.setText(_translate("Form", "Register"))

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        verify = auth([username, password, "login"])
        if verify == "n":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Username or password is wrong. Try again...')
            msg.setWindowTitle("Error")
            msg.exec_()
        elif isinstance(verify, list):
            userKey = password * 5
            cipher = Fernet(base64.urlsafe_b64encode(bytes(userKey[:32], "utf-8")))
            self.switch_window.emit(username, cipher.decrypt(verify[1]), verify[0])

    def register(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if auth([username, password, "register"]) == "y":
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Success")
            msg.setInformativeText('User registered. Login below...')
            msg.setWindowTitle("Success")
            msg.exec_()

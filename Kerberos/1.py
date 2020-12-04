from socket import socket, AF_INET, SOCK_STREAM, gethostname
from PyQt5 import QtWidgets, QtCore

def __init__(self, name, questions):
    super().__init__()
    self.name = name
    self.questions = questions
    self.i = -1
    self.answers = []
    self.widget = QtWidgets.QWidget(self)

    self.progressBar = QtWidgets.QProgressBar(self.widget)
    self.pushButton = QtWidgets.QPushButton(self.widget)
    self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
    self.radioButton = QtWidgets.QRadioButton(self.widget)
    self.radioButton_3 = QtWidgets.QRadioButton(self.widget)
    self.radioButton_4 = QtWidgets.QRadioButton(self.widget)
    self.textEdit = QtWidgets.QTextEdit(self.widget)

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

    # self.label_2.setStyleSheet("color: rgb(231, 231, 231);\n"
    #                             "font: 15pt \"Verdana\";")
    # self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

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
    self.lineEdit.setReadOnly(True)
    self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

    self.progressBar.setObjectName("progressBar")
    self.progressBar.setMinimumSize(QtCore.QSize(0, 40))
    self.progressBar.setStyleSheet('''QProgressBar
                                    {
                                        border: 2px solid white;
                                        border-radius: 5px;
                                        text-align: center;
                                    }
                                    QProgressBar::chunk
                                    {
                                        background-color: #ff0000;
                                        width: 2.15px;
                                        margin: 0.5px;
                                    }''')
    self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.progressBar)

    self.radioButton.setObjectName("radioButton")
    self.radioButton.setMinimumSize(QtCore.QSize(0, 40))
    self.radioButton.setStyleSheet("QRadioButton::indicator::unchecked"
                                        "{"
                                        "width : 20px;"
                                        "height : 20px;"
                                        "}"
                                        "QRadioButton::indicator::checked"
                                        "{"
                                        "width : 25px;"
                                        "height : 25px;"
                                        "}"
                                        "QRadioButton"
                                        "{"
                                        "color : red;"
                                        "font: 24pt Helvetica MS;"
                                        "}")
    self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.radioButton)

    self.radioButton_2.setObjectName("radioButton_2")
    self.radioButton_2.setMinimumSize(QtCore.QSize(0, 40))
    self.radioButton_2.setStyleSheet("QRadioButton::indicator::unchecked"
                                        "{"
                                        "width : 20px;"
                                        "height : 20px;"
                                        "}"
                                        "QRadioButton::indicator::checked"
                                        "{"
                                        "width : 25px;"
                                        "height : 25px;"
                                        "}"
                                        "QRadioButton"
                                        "{"
                                        "color : red;"
                                        "font: 24pt Helvetica MS;"
                                        "}")
    self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.radioButton_2)

    self.radioButton_3.setObjectName("radioButton_3")
    self.radioButton_3.setMinimumSize(QtCore.QSize(0, 40))
    self.radioButton_3.setStyleSheet("QRadioButton::indicator::unchecked"
                                        "{"
                                        "width : 20px;"
                                        "height : 20px;"
                                        "}"
                                        "QRadioButton::indicator::checked"
                                        "{"
                                        "width : 25px;"
                                        "height : 25px;"
                                        "}"
                                        "QRadioButton"
                                        "{"
                                        "color : red;"
                                        "font: 24pt Helvetica MS;"
                                        "}")
    self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.radioButton_3)

    self.radioButton_4.setObjectName("radioButton_4")
    self.radioButton_4.setMinimumSize(QtCore.QSize(0, 40))
    self.radioButton_4.setStyleSheet("QRadioButton::indicator::unchecked"
                                        "{"
                                        "width : 20px;"
                                        "height : 20px;"
                                        "}"
                                        "QRadioButton::indicator::checked"
                                        "{"
                                        "width : 25px;"
                                        "height : 25px;"
                                        "}"
                                        "QRadioButton"
                                        "{"
                                        "color : red;"
                                        "font: 24pt Helvetica MS;"
                                        "}")
    self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.radioButton_4)

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
    self.pushButton.clicked.connect(self.submit)
    self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

    spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    self.formLayout_2.setItem(7, QtWidgets.QFormLayout.SpanningRole, spacerItem)
    self.verticalLayout_3.addLayout(self.formLayout_2)

    spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_3.addItem(spacerItem1)
    self.verticalLayout_2.addLayout(self.verticalLayout_3)

    self.horizontalLayout_3.addWidget(self.widget)
    self.horizontalLayout_3.setStretch(0, 1)
    self.verticalLayout.addLayout(self.horizontalLayout_3)
    QtCore.QMetaObject.connectSlotsByName(self)
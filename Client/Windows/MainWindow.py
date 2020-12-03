from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle(username + " - Client")
        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

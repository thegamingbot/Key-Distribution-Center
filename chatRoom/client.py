import sys
from PyQt5 import QtWidgets
from roomController import Controller

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Controller()
    ex.show_login()
    sys.exit(app.exec_())

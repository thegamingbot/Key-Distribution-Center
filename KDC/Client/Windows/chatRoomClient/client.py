import sys
from PyQt5 import QtWidgets
from roomController import ChatRoomController

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ChatRoomController()
    ex.show_login()
    sys.exit(app.exec_())

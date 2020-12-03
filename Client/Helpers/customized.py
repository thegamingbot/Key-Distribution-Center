from PyQt5 import QtWidgets, QtGui


class PasswordEdit(QtWidgets.QLineEdit):
    CSS = """QtWidgets.QLineEdit {
        border-radius: 0px;
        height: 30px;
        margin: 0px 0px 0px 0px;
    }
    """

    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        self.visibleIcon = QtGui.QIcon("./Resources/icons/eye_on_32x32.png")
        self.hiddenIcon = QtGui.QIcon("./Resources/icons/eye_off_32x32.png")

        self.setEchoMode(QtWidgets.QLineEdit.Password)
        self.togglePasswordAction = self.addAction(self.visibleIcon, QtWidgets.QLineEdit.TrailingPosition)
        self.togglePasswordAction.triggered.connect(self.on_toggle_password_Action)
        self.password_shown = False

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.password_shown = True
            self.togglePasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_shown = False
            self.togglePasswordAction.setIcon(self.visibleIcon)

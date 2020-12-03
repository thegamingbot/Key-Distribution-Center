from Windows.Login import Login
from Windows.MainWindow import MainWindow


class Controller:
    def __init__(self):
        self.login = Login()

    def show_login(self):
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, text):
        self.window = MainWindow(text)
        self.login.close()
        self.window.show()

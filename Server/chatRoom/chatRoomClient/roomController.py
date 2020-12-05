from chat_window import ChatRoom
from login_room import startUI


class Controller:
    def __init__(self):
        self.login = startUI()

    def show_login(self):
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, text):
        self.window = ChatRoom(text)
        self.login.close()
        self.window.show()

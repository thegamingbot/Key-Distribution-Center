from .chat_window import ChatRoom
from .login_room import startUI


class ChatRoomController:
    def __init__(self, ticket):
        self.login = startUI()
        self.ticket = ticket

    def show_login(self):
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, text):
        self.window = ChatRoom(text, self.ticket)
        self.login.close()
        self.window.show()

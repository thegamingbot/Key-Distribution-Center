from .QuizForm import QuizForm
from .resultUI import resultUI
from .startUI import startUI


class QuizController:
    def __init__(self, ticket):
        self.ticket = ticket
        self.login = startUI(ticket)

    def show_login(self):
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, text, questions, client):
        self.window = QuizForm(text, questions, client)
        self.window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.window.show()

    def show_window_two(self, text, client):
        self.window_two = resultUI(text, client)
        self.window.close()
        self.window_two.show()

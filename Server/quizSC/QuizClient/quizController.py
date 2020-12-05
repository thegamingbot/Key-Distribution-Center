from QuizForm import QuizForm
from startUI import startUI

from resultUI import resultUI


class Controller:
    def __init__(self):
        self.login = startUI()

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

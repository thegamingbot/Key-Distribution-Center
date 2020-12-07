from Windows.FileIOClient.ClientGUI import ClientUI
from Windows.QuizClient.quizController import QuizController
from Windows.chatRoomClient.roomController import ChatRoomController
from Windows.Login import Login
from Windows.MainWindow import MainWindow


class Controller:
    def __init__(self):
        self.login = Login()

    def show_login(self):
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, text, sessionKey, TGT):
        self.window = MainWindow(text, sessionKey, TGT)
        self.window.chatApp.connect(self.chatAppS)
        self.window.fileTransfer.connect(self.fileTransferS)
        self.window.quiz.connect(self.quizS)
        self.login.close()
        self.window.show()

    def chatAppS(self, ticket):
        self.chat = ChatRoomController(ticket)
        self.chat.show_login()
        self.window.close()

    def fileTransferS(self, ticket):
        self.file = ClientUI(ticket)
        self.file.show()
        self.window.close()

    def quizS(self, ticket):
        self.quiz = QuizController(ticket)
        self.quiz.show_login()
        self.window.close()

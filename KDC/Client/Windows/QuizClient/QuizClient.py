from PyQt5 import QtWidgets
import sys
from PyQt5.QtGui import QPalette, QColor


# A function to implement dark mode to the application
from quizController import QuizController


def setDarkMode(app):
    # Force the style to be the same on all OSs
    app.setStyle("Fusion")
    # A palette to switch to dark colors
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    # Set the modified palette
    app.setPalette(palette)


def quizClient():
    app = QtWidgets.QApplication(sys.argv)
    setDarkMode(app)
    controller = QuizController()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    quizClient()

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame
from PyQt6.QtCore import QPropertyAnimation, QRect
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties
        self.title = "Codeloop.org - QPropertyAnimation"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        # Initialize window
        self.InitWindow()

    def InitWindow(self):
        # Set window properties
        self.setWindowIcon(QtGui.QIcon("codeloop.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create button
        self.button = QPushButton("Start", self)
        self.button.move(30, 30)
        self.button.clicked.connect(self.doAnimation)

        # Create frame
        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.frame.setGeometry(150, 30, 100, 100)

        # Show window
        self.show()

    def doAnimation(self):
        # Create animation
        self.anim = QPropertyAnimation(self.frame, b"geometry")

        # Duration in milliseconds (10 seconds)
        self.anim.setDuration(10000)

        # Start position and size
        self.anim.setStartValue(QRect(0, 0, 100, 30))

        # End position and size
        self.anim.setEndValue(QRect(250, 250, 100, 30))

        # Start animation
        self.anim.start()  

# Create application instance
App = QApplication(sys.argv)
# Create window instance
window = Window()
# Start application event loop
sys.exit(App.exec())

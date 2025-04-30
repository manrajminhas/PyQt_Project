import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QVBoxLayout,
)
from PyQt6.QtGui import QPixmap

class QuitGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add a label
        label = QLabel("SESSION FINISHED.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        
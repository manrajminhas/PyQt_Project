import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox, QInputDialog, QPlainTextEdit, QVBoxLayout
)
class ListNotesWindow(QWidget):
    """
    Window for displaying the full patient record in a QPlainTextEdit widget.
    """

    def __init__(self, controller, parent, notes):
        super().__init__(parent)

        self.controller = controller
        self.parent_widget = parent
        self.notes = notes

        # Set up the layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title label
        title_label = QLabel("Full Patient Record")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # QPlainTextEdit to display notes
        self.notes_display = QPlainTextEdit()
        self.notes_display.setReadOnly(True)  # Make it read-only
        self.notes_display.setPlainText(self.format_notes())
        self.layout.addWidget(self.notes_display)

        # Back to Menu button
        back_button = QPushButton("Back to Menu")
        back_button.clicked.connect(self.return_to_menu)
        self.layout.addWidget(back_button)

    def format_notes(self):
        """
        Formats the notes for display in the QPlainTextEdit widget.
        """
        return "\n\n".join(
            [f"Note #{note.code}, from {note.timestamp}\n{note.text}" for note in self.notes]
        )

    def return_to_menu(self):
        """
        Navigates back to the appointment main menu.
        """
        from .appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))

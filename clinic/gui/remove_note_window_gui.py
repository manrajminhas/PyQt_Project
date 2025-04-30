import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox, QInputDialog, QVBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt
from clinic.exception import NoCurrentPatientException, IllegalOperationException


class RemoveNoteWindow(QWidget):
    """
    Window for removing a specific note from the patient's record.
    """

    def __init__(self, controller, note_code, parent=None):
        super().__init__(parent)

        self.controller = controller
        self.note_code = note_code
        self.parent_widget = parent

        # Try to fetch the note details
        try:
            self.note = self.controller.search_note(self.note_code)
            if not self.note:
                raise Exception(f"Note #{self.note_code} does not exist.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load note details: {str(e)}")
            self.return_to_menu()
            return

        # Setup GUI layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        title_label = QLabel(f"Remove Note #{self.note_code}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # Note details
        note_details_label = QLabel(f"Note Details:\n\nCode: {self.note.code}\nText: {self.note.text}")
        note_details_label.setStyleSheet("font-size: 14px; color: gray;")
        self.layout.addWidget(note_details_label)

        # Remove Note button
        remove_note_button = QPushButton("Remove Note")
        remove_note_button.clicked.connect(self.confirm_remove_note)
        self.layout.addWidget(remove_note_button)

        # Back to Menu button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.clicked.connect(self.return_to_menu)
        self.layout.addWidget(back_to_menu_button)

    def confirm_remove_note(self):
        """
        Displays a confirmation dialog and removes the note if confirmed.
        """
        confirmation = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove note #{self.note_code}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                if self.controller.delete_note(self.note_code):
                    QMessageBox.information(self, "Success", f"Note #{self.note_code} successfully removed.")
                    self.return_to_menu()
                else:
                    QMessageBox.warning(self, "Failure", f"Failed to remove note #{self.note_code}.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def return_to_menu(self):
        """
        Navigates back to the appointment main menu.
        """
        from .appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))
        else:
            QMessageBox.critical(self, "Error", "Parent widget not set. Cannot navigate back.")
            self.close()
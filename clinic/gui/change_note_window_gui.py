import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox, QInputDialog, QVBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt
from clinic.exception import NoCurrentPatientException, IllegalOperationException


class ChangeNoteWindow(QWidget):
    """
    Window for changing a specific note in the patient's record.
    """

    def __init__(self, controller, note_code, parent=None):
        super().__init__(parent)

        self.controller = controller
        self.note_code = note_code
        self.parent_widget = parent

        # Try to fetch the note before setting up the window
        try:
            self.note = self.controller.search_note(self.note_code)
            if not self.note:
                raise IllegalOperationException(f"Note #{self.note_code} does not exist.")
        except IllegalOperationException as ioe:
            QMessageBox.warning(self, "Error", str(ioe))
            self.return_to_appointment_menu()
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load note details: {str(e)}")
            self.return_to_appointment_menu()
            return

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        title_label = QLabel(f"Change Note #{self.note_code}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # Display current note details
        current_note_label = QLabel("Current Note Details:")
        current_note_label.setStyleSheet("font-size: 14px; color: gray;")
        self.layout.addWidget(current_note_label)

        note_details = QTextEdit()
        note_details.setPlainText(f"Code: {self.note.code}\nText: {self.note.text}")
        note_details.setReadOnly(True)
        self.layout.addWidget(note_details)

        # New note text input
        new_note_label = QLabel("Enter New Note Text:")
        self.layout.addWidget(new_note_label)

        self.new_note_text = QLineEdit()
        self.layout.addWidget(self.new_note_text)

        # Update button
        update_button = QPushButton("Update Note")
        update_button.clicked.connect(self.update_note)
        self.layout.addWidget(update_button)

        # Back to Menu button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.clicked.connect(self.return_to_appointment_menu)
        self.layout.addWidget(back_to_menu_button)

    def update_note(self):
        """
        Handles updating the note with confirmation dialog.
        """
        try:
            new_text = self.new_note_text.text().strip()

            if not new_text:
                QMessageBox.warning(self, "Input Error", "Note text cannot be empty.")
                return

            # Confirm before updating
            confirmation = QMessageBox.question(
                self,
                "Confirm Update",
                f"Are you sure you want to change note #{self.note_code}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if confirmation != QMessageBox.StandardButton.Yes:
                return

            # Update the note in the controller
            if self.controller.update_note(self.note_code, new_text):
                QMessageBox.information(self, "Success", f"Note #{self.note_code} successfully updated.")
                self.return_to_appointment_menu()
            else:
                QMessageBox.warning(self, "Failure", f"Failed to update note #{self.note_code}.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except IllegalOperationException as ioe:
            QMessageBox.warning(self, "Operation Error", str(ioe))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def return_to_appointment_menu(self):
        """
        Navigates back to the appointment main menu GUI.
        """
        from .appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))
            self.deleteLater()  # Ensure the current widget is deleted properly
        else:
            QMessageBox.critical(self, "Error", "Parent widget not set. Cannot navigate back.")
            self.close()  # Close the window as a fallback
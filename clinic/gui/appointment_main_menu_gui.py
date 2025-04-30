from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox, QInputDialog, QVBoxLayout
)
from clinic.exception import NoCurrentPatientException, IllegalAccessException, IllegalOperationException
from clinic.gui.change_note_window_gui import ChangeNoteWindow
from clinic.gui.remove_note_window_gui import RemoveNoteWindow

class AppointMainMenuGUI(QWidget):
    """
    GUI for managing a patient's appointment and records.
    """

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        # Store the controller and parent widget
        self.controller = controller
        self.parent_widget = parent

        # Retrieve the current patient
        self.current_patient = self.controller.get_current_patient()

        # Call appointment menu setup
        self.appointment_menu()

    def appointment_menu(self):
        """
        Creates the layout and adds buttons for the appointment menu.
        """
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add menu content
        title_label = QLabel("MEDICAL CLINIC SYSTEM - APPOINTMENT MENU")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Display patient information
        patient_info_label = QLabel(
            f"PATIENT:\n"
            f"PHN: {self.current_patient.phn}\n"
            f"Name: {self.current_patient.name}\n"
            f"Birth Date: {self.current_patient.birth_date}\n"
            f"Phone: {self.current_patient.phone}\n"
            f"Email: {self.current_patient.email}\n"
            f"Address: {self.current_patient.address}"
        )
        patient_info_label.setStyleSheet("font-size: 14px; color: gray;")
        layout.addWidget(patient_info_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        # Add buttons for appointment menu actions
        add_note_button = QPushButton("Add Note to Patient Record")
        add_note_button.clicked.connect(self.open_add_note)
        layout.addWidget(add_note_button)

        retrieve_notes_button = QPushButton("Retrieve Notes by Text")
        retrieve_notes_button.clicked.connect(self.open_retrieve_notes)
        layout.addWidget(retrieve_notes_button)

        change_note_button = QPushButton("Change Note in Patient Record")
        change_note_button.clicked.connect(self.open_change_note)
        layout.addWidget(change_note_button)

        remove_note_button = QPushButton("Remove Note from Patient Record")
        remove_note_button.clicked.connect(self.open_remove_note)
        layout.addWidget(remove_note_button)

        list_full_record_button = QPushButton("List Full Patient Record")
        list_full_record_button.clicked.connect(self.open_list_full_record)
        layout.addWidget(list_full_record_button)

        finish_appointment_button = QPushButton("Finish Appointment")
        finish_appointment_button.clicked.connect(self.finish_appointment)
        layout.addWidget(finish_appointment_button)

    def open_add_note(self):
        """
        Adds a note to the current patient's record.
        """
        try:
            note_text, ok = QInputDialog.getText(self, "Add Note", "Enter note text:")
            if ok and note_text.strip():
                self.controller.create_note(note_text.strip())
                QMessageBox.information(self, "Success", "Note successfully added to the patient's record!")
            else:
                QMessageBox.warning(self, "Input Error", "Note text cannot be empty.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_retrieve_notes(self):
        """
        Retrieves notes containing specific text from the patient's record.
        """
        try:
            search_text, ok = QInputDialog.getText(self, "Retrieve Notes", "Enter text to search:")
            if not ok or not search_text.strip():  # User canceled or input is empty
                QMessageBox.warning(self, "Input Error", "Search text cannot be empty.")
                return

            notes = self.controller.retrieve_notes(search_text.strip())
            if notes:
                from clinic.gui.retrieve_notes_window_gui import RetrieveNotesWindow  # Delayed import for the notes window
                self.parent_widget.setCentralWidget(RetrieveNotesWindow(self.controller, self.parent_widget, notes, search_text.strip()))
            else:
                QMessageBox.information(self, "No Results", "No notes found matching the search criteria.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_change_note(self):
        """
        Opens a dialog to enter a note number, validates it, and transitions to ChangeNoteWindow if valid.
        """
        try:
            # Step 1: Get the note number (code) from the user
            note_code, ok = QInputDialog.getInt(self, "Change Note", "Enter Note Number (Code):")
            if not ok:  # User canceled the input dialog
                return

            # Step 2: Validate the note exists
            try:
                note = self.controller.search_note(note_code)
                if not note:
                    raise IllegalOperationException(f"Note #{note_code} does not exist.")
            except IllegalOperationException as ioe:
                QMessageBox.warning(self, "Invalid Note", str(ioe))
                return  # Stop further execution if the note is invalid

            # Step 3: Transition to ChangeNoteWindow
            if self.parent_widget:
                self.parent_widget.setCentralWidget(ChangeNoteWindow(self.controller, note_code, self.parent_widget))
            else:
                QMessageBox.critical(self, "Error", "Parent widget not set. Cannot open ChangeNoteWindow.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_remove_note(self):
        """
        Opens a dialog to enter a note number, validates it, and transitions to RemoveNoteWindow if valid.
        """
        try:
            # Step 1: Get the note number (code) from the user
            note_code, ok = QInputDialog.getInt(self, "Remove Note", "Enter Note Number (Code):")
            if not ok:  # User canceled the input dialog
                return

            # Step 2: Validate the note exists
            try:
                note = self.controller.search_note(note_code)
                if not note:
                    raise IllegalOperationException(f"Note #{note_code} does not exist.")
            except IllegalOperationException as ioe:
                QMessageBox.warning(self, "Invalid Note", str(ioe))
                return  # Stop further execution if the note is invalid

            # Step 3: Transition to RemoveNoteWindow
            if self.parent_widget:
                from clinic.gui.remove_note_window_gui import RemoveNoteWindow  # Delayed import
                self.parent_widget.setCentralWidget(RemoveNoteWindow(self.controller, note_code, self.parent_widget))
            else:
                QMessageBox.critical(self, "Error", "Parent widget not set. Cannot open RemoveNoteWindow.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_list_full_record(self):
        """
        Lists the full record of the current patient in a new window with a QPlainTextEdit widget.
        """
        try:
            notes = self.controller.list_notes()
            if notes:
                from clinic.gui.list_notes_window_gui import ListNotesWindow  # Delayed import for the notes window
                self.parent_widget.setCentralWidget(ListNotesWindow(self.controller, self.parent_widget, notes))
            else:
                QMessageBox.information(self, "No Notes", "The patient's record is empty.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def finish_appointment(self):
        """
        Finishes the current appointment and returns to the main menu.
        """
        try:
            self.controller.unset_current_patient()
            self.back_to_main_menu()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def back_to_main_menu(self):
        """
        Navigates back to the main menu GUI.
        """
        from .mainmenu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
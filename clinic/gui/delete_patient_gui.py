from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from clinic.exception import IllegalAccessException

class DeletePatientGUI(QWidget):
    def __init__(self, app_handler, parent_window=None):
        super().__init__(parent_window)

        # Store the handler and parent window reference
        self.app_handler = app_handler
        self.parent_window = parent_window

        # Create the main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title Section
        title = QLabel("Patient Lookup")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: darkgreen;")
        layout.addWidget(title)

        # Layout customization
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(12)

        # Prompt for PHN
        self.label_phn = QLabel("Enter the Patient's PHN:")
        layout.addWidget(self.label_phn)

        # Input field for PHN
        self.input_phn = QLineEdit()
        self.input_phn.setPlaceholderText("Type the PHN here...")
        layout.addWidget(self.input_phn)

        # Button to initiate search
        btn_search = QPushButton("Search")
        btn_search.clicked.connect(self.search_patient)
        layout.addWidget(btn_search)

        # Button to return to the main menu
        btn_return = QPushButton("Back to Main Menu")
        btn_return.clicked.connect(self.navigate_to_main_menu)
        layout.addWidget(btn_return)

    def search_patient(self):
        """
        Handles the patient lookup logic using the provided PHN.
        """
        try:
            # Retrieve and validate PHN input
            entered_phn = int(self.input_phn.text().strip())

            # Query the patient information
            patient = self.app_handler.delete_patient(entered_phn)
            if patient:
                # Display patient information
                QMessageBox.information(
                    self,
                    "Patient deleted successfully"
                )
            else:
                # Notify if no patient found
                QMessageBox.warning(self, "No Match", "No patient found with the entered PHN.")

        except ValueError:
            # Handle invalid input
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except IllegalAccessException:
            # Handle access control issues
            QMessageBox.critical(self, "Access Denied", "You must be logged in to search for a patient.")
        except Exception as e:
            # Catch all other exceptions
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{e}")

    def navigate_to_main_menu(self):
        """
        Redirects to the main menu interface.
        """
        from .mainmenu_gui import MainMenuGUI  # Delayed import to prevent circular dependency
        if self.parent_window:
            self.parent_window.setCentralWidget(MainMenuGUI(self.app_handler, self.parent_window))

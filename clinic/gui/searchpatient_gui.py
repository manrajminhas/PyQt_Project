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

class PatientSearchWidget(QWidget):
    def __init__(self, app_controller, main_window=None):
        super().__init__(main_window)

        # Store the controller and main window reference
        self.app_controller = app_controller
        self.main_window = main_window

        # Layout setup
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title Label
        heading_label = QLabel("Find Patient by PHN")
        heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading_label.setStyleSheet("font-size: 20px; font-weight: bold; color: navy;")
        main_layout.addWidget(heading_label)

        # Set layout padding and spacing
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)

        # PHN Input Section
        self.phn_prompt = QLabel("Please enter the Personal Health Number (PHN):")
        main_layout.addWidget(self.phn_prompt)

        self.phn_entry = QLineEdit()
        self.phn_entry.setPlaceholderText("Enter PHN here...")
        main_layout.addWidget(self.phn_entry)

        # Search Button
        search_btn = QPushButton("Find Patient")
        search_btn.clicked.connect(self.handle_patient_search)
        main_layout.addWidget(search_btn)

        # Return to Menu Button
        menu_btn = QPushButton("Return to Main Menu")
        menu_btn.clicked.connect(self.return_to_main_menu)
        main_layout.addWidget(menu_btn)

    def handle_patient_search(self):
        """
        Processes the PHN input and searches for the patient.
        """
        try:
            # Get and validate PHN
            phn_value = int(self.phn_entry.text().strip())

            # Search for patient using the controller
            patient_data = self.app_controller.search_patient(phn_value)
            if patient_data:
                # Show details if patient is found
                QMessageBox.information(
                    self,
                    "Patient Found",
                    f"PHN: {patient_data.phn}\n"
                    f"Name: {patient_data.name}\n"
                    f"Date of Birth: {patient_data.birth_date}\n"
                    f"Contact: {patient_data.phone}\n"
                    f"Email: {patient_data.email}\n"
                    f"Address: {patient_data.address}"
                )
            else:
                # Notify if patient not found
                QMessageBox.warning(self, "Not Found", "No patient matches the entered PHN.")

        except ValueError:
            # Notify about invalid input
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid numeric PHN.")
        except IllegalAccessException:
            # Notify about illegal access
            QMessageBox.critical(self, "Access Denied", "You must log in to perform this action.")
        except Exception as error:
            # Catch any unexpected exceptions
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{error}")

    def return_to_main_menu(self):
        """
        Switches back to the main menu interface.
        """
        from .mainmenu_gui import MainMenuGUI  # Import delayed to avoid circular dependency
        if self.main_window:
            self.main_window.setCentralWidget(MainMenuGUI(self.app_controller, self.main_window))
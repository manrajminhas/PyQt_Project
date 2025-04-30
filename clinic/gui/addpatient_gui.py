from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from clinic.exception import IllegalAccessException
from clinic.exception import IllegalOperationException

class AddPatientGUI(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)

        # calling controller class for future use
        self.controller = controller
        self.parent_widget = parent

        # self.controller.logged_in = True

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title_label = QLabel("ADD PATIENT")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        # PHN
        self.phn_label = QLabel("Personal Health Number (PHN):")
        layout.addWidget(self.phn_label)
        self.phn_input = QLineEdit()
        layout.addWidget(self.phn_input)

        # Full Name
        self.name_label = QLabel("Full Name:")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Birth Date
        self.birth_date_label = QLabel("Birth Date (YYYY-MM-DD):")
        layout.addWidget(self.birth_date_label)
        self.birth_date_input = QLineEdit()
        layout.addWidget(self.birth_date_input)

        # Phone Number
        self.phone_label = QLabel("Phone Number:")
        layout.addWidget(self.phone_label)
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_input)

        # Email
        self.email_label = QLabel("Email:")
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        # Address
        self.address_label = QLabel("Address:")
        layout.addWidget(self.address_label)
        self.address_input = QLineEdit()
        layout.addWidget(self.address_input)

        # Add Patient Button
        self.add_patient_button = QPushButton("Add Patient")
        self.add_patient_button.clicked.connect(self.add_patient)
        layout.addWidget(self.add_patient_button)

        # Back to main menu button
        self.back_to_menu = QPushButton("Back to Menu")
        self.back_to_menu.clicked.connect(self.back_to_menu_func)
        layout.addWidget(self.back_to_menu)

    def add_patient(self):
        """
        Handles adding a new patient.
        """
        try:
            # Extract and validate inputs
            phn = int(self.phn_input.text())
            name = self.name_input.text()
            birth_date = self.birth_date_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()
            address = self.address_input.text()

            # Ensure all fields are filled
            if not all([name, birth_date, phone, email, address]):
                raise ValueError("All fields must be filled out.")

            # Call the controller to create a patient
            self.controller.create_patient(phn, name, birth_date, phone, email, address)
            
            # Success message
            QMessageBox.information(self, "Patient Added", "Patient successfully added!")
            self.phn_input.clear()
            self.name_input.clear()
            self.birth_date_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.address_input.clear()

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to add a patient.")
        except IllegalOperationException as ioe:
            QMessageBox.warning(self, "Operation Error", str(ioe))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
        
    def back_to_menu_func(self):
        from .mainmenu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
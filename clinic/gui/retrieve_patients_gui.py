from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableView, QHeaderView
)
from clinic.exception import IllegalAccessException


class PatientTableModel(QAbstractTableModel):
    def __init__(self, patients=None):
        super().__init__()
        self.patients = patients or []
        self.headers = ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"]

    def rowCount(self, parent=None):
        return len(self.patients)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None

        patient = self.patients[index.row()]
        column = index.column()

        # Handle display role
        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return patient.phn
            elif column == 1:
                return patient.name
            elif column == 2:
                return patient.birth_date
            elif column == 3:
                return patient.phone
            elif column == 4:
                return patient.email
            elif column == 5:
                return patient.address

        # Handle text alignment role (center the content)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None


class RetrievePatientGUI(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)

        # Store the controller and parent widget
        self.controller = controller
        self.parent_widget = parent

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title_label = QLabel("RETRIEVE PATIENTS BY NAME")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        # Name Input
        self.name_label = QLabel("Enter Patient's Name (or part of the name):")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Search Button
        search_button = QPushButton("Retrieve Patients")
        search_button.clicked.connect(self.retrieve_patients)
        layout.addWidget(search_button)

        # Patient Table View
        self.patient_table = QTableView()
        self.patient_model = PatientTableModel()
        self.patient_table.setModel(self.patient_model)
        self.patient_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.patient_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.patient_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.patient_table.setWordWrap(True)  # Enable word wrapping
        self.patient_table.resizeRowsToContents()  # Adjust row height to fit wrapped content

        # Connect sectionResized signal to resizeRowsToContents slot
        header = self.patient_table.horizontalHeader()
        header.sectionResized.connect(self.patient_table.resizeRowsToContents)  # Adjust rows when columns resize

        # Use QHeaderView to access ResizeMode
        header.setStretchLastSection(True)  # Stretch last column (address)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # PHN
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name (stretch for long names)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Birth Date
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Phone
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Email (stretch for long emails)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  # Address

        layout.addWidget(self.patient_table)

        # Back to main menu button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.clicked.connect(self.back_to_menu_func)
        layout.addWidget(back_to_menu_button)

    def retrieve_patients(self):
        """
        Handles retrieving patients by name.
        """
        try:
            # Extract name input
            search_string = self.name_input.text().strip()

            if not search_string:
                QMessageBox.warning(self, "Input Error", "Please enter a name to search.")
                return

            # Call the controller to retrieve patients
            patients = self.controller.retrieve_patients(search_string)

            if patients:
                # Update the table model with retrieved patients
                self.patient_model = PatientTableModel(patients)
                self.patient_table.setModel(self.patient_model)
                self.adjust_table()
            else:
                QMessageBox.information(self, "No Results", "No patients found matching the search criteria.")
                self.patient_model = PatientTableModel()  # Clear table
                self.patient_table.setModel(self.patient_model)
                self.adjust_table()

        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to retrieve patients.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def adjust_table(self):
        """
        Adjusts the table rows and column sizes to fit the content, including wrapping text for Name, Email, and Address.
        """
        self.patient_table.resizeRowsToContents()  # Adjust rows based on content
        self.patient_table.horizontalHeader().setStretchLastSection(True)  # Stretch the Address column

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from .mainmenu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))

from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableView, QMessageBox


class PatientTableModel(QAbstractTableModel):
    """
    Custom TableModel for displaying patient data in QTableView.
    """

    def __init__(self, patients, parent=None):
        super().__init__(parent)
        self.patients = patients
        self.headers = ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"]

    def rowCount(self, parent=None):
        return len(self.patients)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            patient = self.patients[index.row()]
            column = index.column()
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

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return section + 1


class ListPatientsGUI(QWidget):
    """
    GUI for displaying all patients using QTableView.
    """

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        # Store the controller and parent widget
        self.controller = controller
        self.parent_widget = parent

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title_label = QLabel("ALL PATIENTS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        # Table view for patients
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        # Load patients and set up the model
        try:
            patients = self.controller.patient_dao.list_patients()
            if patients:
                self.model = PatientTableModel(patients)
                self.table_view.setModel(self.model)
                self.table_view.resizeColumnsToContents()
            else:
                QMessageBox.information(self, "No Patients", "There are no patients in the system.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

        # Back to Main Menu Button
        self.back_to_menu_button = QPushButton("Back to Menu")
        self.back_to_menu_button.clicked.connect(self.back_to_menu_func)
        layout.addWidget(self.back_to_menu_button)

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.mainmenu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from clinic.gui.addpatient_gui import AddPatientGUI
from clinic.gui.searchpatient_gui import PatientSearchWidget
from clinic.gui.retrieve_patients_gui import RetrievePatientGUI
from clinic.gui.update_patient_gui import UpdatePatientGUI
from clinic.gui.delete_patient_gui import DeletePatientGUI
from clinic.gui.quit_confirmation_gui import QuitConfirmationDialog
from clinic.gui.start_appointment_gui import StartAppointmentGUI
from clinic.gui.list_patients_gui import ListPatientsGUI

class MainMenuGUI(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)

        # Calling the controller class for future use
        self.controller = controller
        self.parent_widget = parent

        # Initialize the main menu
        self.main_menu()

    def main_menu(self):
        """Creates and sets up the main menu layout."""
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add main menu content
        title_label = QLabel("Welcome to the Medical Clinic System Main Menu!")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)

        # Configure layout margins and spacing
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        # Add "Add New Patient" button
        add_patient_button = QPushButton("Add New Patient")
        add_patient_button.clicked.connect(self.open_add_patient_gui)
        layout.addWidget(add_patient_button)

        # Add "Search Patient by PHN" button
        search_patient_button = QPushButton("Search Patient by PHN")
        search_patient_button.clicked.connect(self.open_search_patient_gui)
        layout.addWidget(search_patient_button)

        # Add "Retrieve Patients by Name" button
        retrieve_patients_button = QPushButton("Retrieve Patients by Name")
        retrieve_patients_button.clicked.connect(self.open_retrieve_patients_gui)
        layout.addWidget(retrieve_patients_button)

        # Add "Change Patient Data" button
        update_patient_data_button = QPushButton("Change Patient Data")
        update_patient_data_button.clicked.connect(self.open_update_patient_data_gui)
        layout.addWidget(update_patient_data_button)

        # Add "Delete Patient" button
        delete_patient_button = QPushButton("Delete Patient")
        delete_patient_button.clicked.connect(self.open_delete_patient_gui)
        layout.addWidget(delete_patient_button)

        
        # List all patients
        list_all_patients_button = QPushButton("List All Patients")
        list_all_patients_button.clicked.connect(self.open_list_patients_gui)
        layout.addWidget(list_all_patients_button)


        # Start appointment with patient
        start_appointment_button = QPushButton("Start Appointment with Patient")
        start_appointment_button.clicked.connect(self.start_appointment)
        layout.addWidget(start_appointment_button)

        # Add "Log Out" button (integrating quit functionality)
        log_out_button = QPushButton("Log Out")
        log_out_button.clicked.connect(self.logout_with_confirmation)
        layout.addWidget(log_out_button)

    def open_add_patient_gui(self):
        """Opens AddPatientGUI."""
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AddPatientGUI(self.controller, self.parent_widget))

    def open_search_patient_gui(self):
        """Opens PatientSearchWidget."""
        if self.parent_widget:
            self.parent_widget.setCentralWidget(PatientSearchWidget(self.controller, self.parent_widget))

    def open_retrieve_patients_gui(self):
        """Opens RetrievePatientGUI."""
        if self.parent_widget:
            self.parent_widget.setCentralWidget(RetrievePatientGUI(self.controller, self.parent_widget))

    def open_update_patient_data_gui(self):
        """Opens UpdatePatientGUI."""
        if self.parent_widget:
            self.parent_widget.setCentralWidget(UpdatePatientGUI(self.controller, self.parent_widget))

    def open_delete_patient_gui(self):
        """Opens DeletePatientGUI."""
        if self.parent_widget:
            self.parent_widget.setCentralWidget(DeletePatientGUI(self.controller, self.parent_widget))

    
    def open_list_patients_gui(self):
        '''
        opens open_list_all_patients_gui
        '''
        if self.parent_widget:
            self.parent_widget.setCentralWidget(ListPatientsGUI(self.controller, self.parent_widget))


    def start_appointment(self):
        '''
        opens start_appointment_gui
        '''
        if self.parent_widget:
            self.parent_widget.setCentralWidget(StartAppointmentGUI(self.controller, self.parent_widget))

    def logout_with_confirmation(self):
        """Shows confirmation dialog before logging out."""
        #changes = self.controller.get_session_changes()
        changes = ""
        dialog = QuitConfirmationDialog(changes, self)
        if dialog.exec():  # If user confirms
            if self.parent():  # Check if the parent exists
                self.parent().login_screen()  # Set to login screen

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox, QInputDialog, QVBoxLayout
)
from clinic.exception import IllegalAccessException


class StartAppointmentGUI(QWidget):
    """
    GUI for starting an appointment by searching for a patient using their PHN.
    """

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        # Store the controller and parent widget
        self.controller = controller
        self.parent_widget = parent

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Set up the search view
        self.create_search_view()

    def create_search_view(self):
        """
        Displays the initial search interface for starting an appointment.
        """
        # Clear the layout
        self.clear_layout()

        # Title
        title_label = QLabel("SEARCH START APPOINTMENT")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # PHN Input
        self.phn_label = QLabel("Personal Health Number (PHN):")
        self.layout.addWidget(self.phn_label)
        self.phn_input = QLineEdit()
        self.layout.addWidget(self.phn_input)

        # Search Button
        search_button = QPushButton("Search Patient")
        search_button.clicked.connect(self.search_patient)
        self.layout.addWidget(search_button)

        # Back to Main Menu Button
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.clicked.connect(self.back_to_menu_func)
        self.layout.addWidget(back_to_menu_button)

    def search_patient(self):
        """
        Searches for a patient by PHN and transitions to the appointment menu.
        """
        try:
            phn = int(self.phn_input.text().strip())
            patient = self.controller.search_patient(phn)

            if patient:
                # Set the current patient in the Controller
                self.controller.set_current_patient(phn)

                # Navigate to the appointment menu
                self.open_appointment_menu()
            else:
                QMessageBox.warning(self, "Not Found", "No patient found with the provided PHN.")

        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to search for patients.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_appointment_menu(self):
        """
        Opens the appointment menu after a successful patient search.
        """
        from .appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.
        """
        from .mainmenu_gui import MainMenuGUI  # Delayed import to avoid circular imports
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))

    def clear_layout(self):
        """
        Clears all widgets from the current layout.
        """
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
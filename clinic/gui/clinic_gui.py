import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont

from .mainmenu_gui import MainMenuGUI
from .quit_gui import QuitGUI
from clinic.controller import Controller
from clinic.exception import InvalidLoginException


class ClinicGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set title
        self.width = 1024
        self.height = 768
        self.setWindowTitle("MEDICAL CLINIC SYSTEM")
        self.setGeometry(*self.get_center(self.width, self.height))
        self.setFixedSize(1024, 768)  # Fixed size to prevent resizing

        # Load stylesheet
        self.setStyleSheet(open("clinic/gui/style.qss", "r").read())

        # Calling controller class for future use
        self.controller = Controller(autosave=True)

        self.login_screen()  # Call login screen

    def get_center(self, window_width, window_height):
        """Calculate the center position of the screen for the window."""
        screen = QApplication.primaryScreen().availableGeometry()
        screen_center_x = screen.width() / 2
        screen_center_y = screen.height() / 2

        x = int(screen_center_x - window_width / 2)
        y = int(screen_center_y - window_height / 2)

        return (x, y, window_width, window_height)

    def login_screen(self):
        # Set to false because you can only come here after logging out
        self.controller.logged_in = False

        # Create the central widget and set it
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the main screen
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Add a medical system title to the layout
        medical_system_title = QLabel("MEDICAL CLINIC SYSTEM")
        medical_system_title.setStyleSheet("font-size: 64px; font-weight: bold; color: #ffffff;")
        medical_system_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(medical_system_title)

        # Add spacer to push the login form to the center vertically
        main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Create a grid layout for the login form and center it horizontally
        form_widget = QWidget()
        form_layout = QGridLayout()
        form_widget.setLayout(form_layout)
        form_widget.setMaximumWidth(400)  # Set a maximum width for the form
        main_layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Username label with larger font
        username_label = QLabel("Username:")
        username_font = QFont("Arial", 25, QFont.Weight.Bold)  # Set the font size to 14 and make it bold
        username_label.setFont(username_font)
        form_layout.addWidget(username_label, 0, 0, Qt.AlignmentFlag.AlignRight)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedSize(450,60)  # Set a fixed width to shorten the dialog box
        form_layout.addWidget(self.username_input, 0, 1)

        # Password label with larger font
        password_label = QLabel("Password:")
        password_label.setFont(username_font)  # Use the same font as username label
        form_layout.addWidget(password_label, 1, 0, Qt.AlignmentFlag.AlignRight)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedSize(450,60)  # Set a fixed width to shorten the dialog box
        form_layout.addWidget(self.password_input, 1, 1)

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()  # Initially hidden
        form_layout.addWidget(self.error_label, 2, 0, 1, 2)

        # Add buttons for login and quit
        login_button = QPushButton("Log In")
        login_button.setFixedWidth(120)  # Set fixed width for consistency
        login_button.clicked.connect(self.login)
        form_layout.addWidget(login_button, 3, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        quit_button = QPushButton("Quit")
        quit_button.setFixedWidth(120)  # Set fixed width for consistency
        quit_button.clicked.connect(self.quit)
        form_layout.addWidget(quit_button, 3, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        login_button.setFixedSize(150, 50)  # Set width to 150 pixels and height to 50 pixels
        quit_button.setFixedSize(150, 50)    # Set width to 150 pixels and height to 50 pixels


        # Add another spacer to push the form to the center
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def login(self):
        """
        Handles the login button click event.
        Verifies the username and password using the Controller.
        Opens the MainMenuGUI upon successful login.
        """
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            if self.controller.login(username, password):
                self.error_label.hide()  # Hide the error label on successful login
                self.controller.logged_in = True  # User has successfully logged in
                self.open_main_menu()
            else:
                self.show_error_message("Invalid credentials.")
                self.shake_dialog()
        except InvalidLoginException:
            self.show_error_message("Login Failed. Invalid Username or Password.")
            self.username_input.clear()
            self.password_input.clear()
            self.shake_dialog()

    def show_error_message(self, message):
        """Displays an error message under the dialog box."""
        self.error_label.setText(message)
        self.error_label.show()

    def shake_dialog(self):
        """Shake the dialog box left and right."""

        self.user_anim = QPropertyAnimation(self.username_input, b"geometry")
        self.pass_anim = QPropertyAnimation(self.password_input, b"geometry")

        current_pos_username = self.username_input.geometry()
        current_pos_password = self.password_input.geometry()

        # Duration in milliseconds (150 ms for a quick shake)
        self.user_anim.setDuration(150)
        self.pass_anim.setDuration(150)

        # Set keyframes for the animation for shaking effect
        self.user_anim.setStartValue(current_pos_username)
        self.user_anim.setKeyValueAt(0.25, current_pos_username.translated(5, 0))
        self.user_anim.setKeyValueAt(0.5, current_pos_username.translated(-5, 0))
        self.user_anim.setKeyValueAt(0.75, current_pos_username.translated(5, 0))
        self.user_anim.setEndValue(current_pos_username)

        self.pass_anim.setStartValue(current_pos_password)
        self.pass_anim.setKeyValueAt(0.25, current_pos_password.translated(5, 0))
        self.pass_anim.setKeyValueAt(0.5, current_pos_password.translated(-5, 0))
        self.pass_anim.setKeyValueAt(0.75, current_pos_password.translated(5, 0))
        self.pass_anim.setEndValue(current_pos_password)

        # Start animation
        self.user_anim.start()
        self.pass_anim.start()

    def open_main_menu(self):
        """Opens the main menu."""
        self.setCentralWidget(MainMenuGUI(self.controller, self))

    def quit(self):
        """Quits the application."""
        self.setCentralWidget(QuitGUI(self))


def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

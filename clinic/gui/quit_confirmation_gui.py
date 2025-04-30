from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout

class QuitConfirmationDialog(QDialog):
    def __init__(self, changes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Quit")
        self.setModal(True)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title_label = QLabel("You are about to logout from this session.")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        # Changes log
        changes_label = QLabel("Changes made during this session:")
        layout.addWidget(changes_label)

        changes_view = QTextEdit()
        changes_view.setReadOnly(True)
        changes_view.setText("\n".join(changes) if changes else "No changes made during this session.")
        layout.addWidget(changes_view)

        # Buttons
        button_layout = QHBoxLayout()
        quit_button = QPushButton("Logout")
        quit_button.clicked.connect(self.accept)  # Close dialog and proceed
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Close dialog and cancel
        button_layout.addWidget(quit_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

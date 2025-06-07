Medical Clinic System GUI

This personal project demonstrates a Model-View-Controller (MVC) approach by adding a PyQt6 graphical interface to an existing clinic management back end.

Project Structure

a5/
├── clinic/
│   ├── controller.py           # Core controller logic
│   ├── patient.py              # Patient model
│   ├── patient_record.py       # Record model
│   ├── note.py                 # Note model
│   ├── dao/
│   │   ├── patient_dao_json.py # JSON persistence layer
│   │   ├── note_dao_pickle.py  # Pickle persistence layer
│   │   ├── patient_encoder.py  # Model serialization
│   │   └── patient_decoder.py  # Model deserialization
│   └── cli/                    # Prototype command-line UI
│       └── __main__.py         # Launch with `python3 -m clinic cli`
├── clinic/gui/                 # PyQt6 GUI modules
│   ├── clinic_gui.py           # Main window (ClinicGUI)
│   └── ...                     # Additional windows, widgets, layouts
└── tests/                      # Unit tests (optional)

Requirements

Python 3.9 (features compatible with 3.9+)

PyQt6 framework:

pip install PyQt6

Installation & Setup

Clone the repo and navigate into the a5 directory.

Ensure all backend files and DAOs are present under clinic/ and clinic/dao/.

Install PyQt6 if not already:

pip install PyQt6

Usage

Command-Line Prototype

Run the prototype CLI to explore controller interactions:

python3 -m clinic cli

Follow prompts to log in, manage patients, appointments, and notes.

Graphical Interface

Launch the PyQt6 GUI:

python3 -m clinic gui

Login/Logout

Search & CRUD patients (displayed in a QTableView)

View & edit notes (displayed in a QPlainTextEdit)

MVC Highlights

Model: patient.py, patient_record.py, note.py encapsulate data.

View: clinic/gui contains UI classes decoupled from business logic.

Controller: controller.py mediates between view and model.

Contributing & Workflow

Develop features on a separate branch, merge when stable.

Commit frequently with descriptive messages.

Manual testing through the GUI to verify data persistence and UI behavior.

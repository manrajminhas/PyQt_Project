
from .patient import Patient
from .patient_record import PatientRecord
from .note import Note
from datetime import datetime
import hashlib
from clinic.exception import DuplicateLoginException, IllegalAccessException, IllegalOperationException, InvalidLoginException, InvalidLogoutException,NoCurrentPatientException
from clinic.dao import PatientDAOJSON
from clinic.dao import NoteDAOPickle
class Controller:
    """
    Controller class to manage patient records, login, and note management for a clinic system.
    """
    def __init__(self,autosave:bool):
        """
        Initializes the Controller with an empty patient dictionary, 
        login status, and current patient information.
        """
        #self.patients = {}  # Dictionary to store patients by PHN
        self.logged_in = False
        self.username = None
        self.current_patient = None
        self.users = {}
        self.users_read = False
        self.autosave = autosave

        self.patient_dao = PatientDAOJSON(autosave = autosave)  # Patient DAO for patient data management
        self.load_users()
        
    # User story 1
    def login(self, username: str, password: str) -> bool:
        """
        Logs in a user with valid credentials.
        
        Parameters:
            username (str): The username for login.
            password (str): The password for login.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        
        # Check if already logged in
        if self.logged_in:
            #print("Already logged in.")
            raise DuplicateLoginException
        
        if username in self.users:
            
            input_password = str(hashlib.sha256(password.encode()).hexdigest())
            if input_password == self.users[username]:
                self.logged_in = True  # Indicate the user is now logged in
                self.username = username
                return True

            else:
                raise InvalidLoginException            
        
        else:
            raise InvalidLoginException

    # User story 2
    def logout(self):
        """
        Logs out the current user.

        Returns:
            bool: True if logout is successful, False if no user is logged in.
        """
        if not self.logged_in:
            raise InvalidLogoutException
            
        self.logged_in = False
        self.username = None
        return True

    # User story 3
    def search_patient(self, phn) -> Patient:
        """
        Searches for a patient by personal health number (PHN).

        Args:
            phn (str): The personal health number of the patient.

        Returns:
            Patient or None: The found patient, or None if not found.
        """
        if not self.logged_in:
            #print("You must be logged in to search for patients.")
            raise IllegalAccessException
        
        return self.patient_dao.search_patient(phn)

            


    # User story 4
    def create_patient(self, phn, name, birth_date, phone, email, address):
        """
        Creates a new patient record.

        Args:
            phn (str): The personal health number of the patient.
            name (str): The name of the patient.
            birth_date (str): The birth date of the patient.
            phone (str): The phone number of the patient.
            email (str): The email address of the patient.
            address (str): The address of the patient.

        Returns:
            Patient or None: The created patient, or None if the patient already exists.
        """
        if not self.logged_in:
            #print("Please log in first")
            raise IllegalAccessException
        if self.patient_dao.patients and phn in self.patient_dao.patients:
            #print("Patient already exists")
            raise IllegalOperationException
        
        patient = Patient(phn,name,birth_date,phone,email,address,autosave = self.autosave)
        self.patient_dao.create_patient(patient)
        
        return patient

    # User story 8
    def list_patients(self) -> list[Patient]:
        """
        Lists all patients in the system.

        Returns:
            list: A list of all patients, or an empty list if no patients found.
        """
        if not self.logged_in:
            #print("Please log in first.")
            raise IllegalAccessException

        if not self.patient_dao.patients:
            #print("No patients found")
            return []

        return self.patient_dao.list_patients()

    # User story 5
    def retrieve_patients(self, name:str) -> list[Patient]:
        """
        Retrieves patients by their name.

        Args:
            name (str): The name to search for.

        Returns:
            list: A list of matching patients, or an empty list if none found.
        """
        if not self.logged_in:
            #print("Please log in first.")
            raise IllegalAccessException

    
        return self.patient_dao.retrieve_patients(name)

        
    def update_patient(self, phn, new_phn=None, name=None, birth_date=None, phone=None, email=None, address=None) -> bool:
        """
        Updates the details of an existing patient.

        Args:
            phn (str): The current personal health number of the patient.
            new_phn (str, optional): A new personal health number for the patient.
            name (str, optional): The new name of the patient.
            birth_date (str, optional): The new birth date of the patient.
            phone (str, optional): The new phone number of the patient.
            email (str, optional): The new email address of the patient.
            address (str, optional): The new address of the patient.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        if not self.logged_in:
            raise IllegalAccessException

        # Find the patient using the current PHN
        patient = self.patient_dao.search_patient(phn)
        if patient is None:
            raise IllegalOperationException

        if self.current_patient is not None and phn == self.current_patient.phn:
            raise IllegalOperationException

        # If new_phn is provided and differs from the current phn, handle the PHN change
        if new_phn and new_phn != phn:
            # Check if new_phn already exists to prevent duplicate PHNs
            if self.patient_dao.search_patient(new_phn) is not None:
                raise IllegalOperationException  # new_phn already exists
            
            # Delete the old PHN entry and create a new entry with updated PHN
            self.patient_dao.delete_patient(phn)
            patient.phn = new_phn  # Update the patient's PHN attribute
            self.patient_dao.create_patient(patient)

        # Update other patient details if provided
        if name is not None:
            patient.name = name
        if birth_date is not None:
            patient.birth_date = birth_date
        if phone is not None:
            patient.phone = phone
        if email is not None:
            patient.email = email
        if address is not None:
            patient.address = address

        # Save the updated patient information
        self.patient_dao.update_patient(patient.phn, patient)

        return True



    # User story 7
    def delete_patient(self,phn) -> bool:
        """
        Deletes a patient by their personal health number.

        Args:
            phn (str): The personal health number of the patient to delete.

        Returns:
            bool: True if the patient was deleted successfully, False otherwise.
        """

        #print("entered delete patient")
        #print("delete patients before deletion: ",self.patient_dao.patients)
        if not self.logged_in:
            #print("You must be logged in to delete patients.")
            raise IllegalAccessException
        
        if self.current_patient and phn == self.current_patient.phn:
            #print("Cannot delete the currently selected patient. Please deselect first")
            raise IllegalOperationException
        
        if phn in self.patient_dao.patients:
            self.patient_dao.delete_patient(phn)
            #print(f"Patient with PHN {phn} deleted successfully")
            return True
        else:
            #print("Patient not found to delete")
            raise IllegalOperationException

    # User Story 9
    def set_current_patient(self,phn) -> None:
        """
        Sets the currently selected patient.

        Args:
            phn (str): The personal health number of the patient to set as current.

        Returns:
            None
        """
        patient = self.search_patient(phn)

        if patient:
            
            self.current_patient = patient
            #print(f"Current patient set to {patient.name}")

        else:
            raise IllegalOperationException
            #print("Patient not found")

    # User Story 9
    def get_current_patient(self) -> Patient:
        """
        Gets the currently selected patient.

        Returns:
            Patient or None: The currently selected patient, or None if no patient is selected.
        """
        if not self.logged_in:
            #print("please log in first")
            raise IllegalAccessException
        
        return self.current_patient

# controller.py (within the Controller class)

    def unset_current_patient(self) -> bool:
        """
        Deselects the current patient.

        Returns:
            bool: True if successfully deselected, False if no patient was selected.
        """
        if not self.logged_in:
            #print("Please log in first.")
            raise IllegalAccessException
        if self.current_patient is None:
            #print("No patient is currently selected.")
            raise IllegalOperationException

        # Unset the current patient
        self.current_patient = None
        #print("Current patient deselected.")
        return True


    def add_note_to_patient(self, phn, details) -> Note:
        """
        Adds a new note to a patient's record.

        Args:
            phn (str): The personal health number of the patient.
            details (str): The details of the note to add.

        Returns:
            Note or None: The created note, or None if the patient was not found.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        patient_record = self.get_patient_record(phn)
        if patient_record:
            return patient_record.add_note(details)
        return None

    def create_note(self, text) -> Note:
        """
        Creates a new note for the currently selected patient.

        Args:
            text (str): The text of the note.

        Returns:
            Note or None: The created note, or None if the user is not logged in or no patient is selected.
        """
        if not self.logged_in:
            #print("please login first")
            raise IllegalAccessException
        if not self.current_patient:
            #print("No patient is currently selected. Please select a patient first")
            raise NoCurrentPatientException
        
        phn = self.current_patient.phn

        return self.current_patient.create_note(text)
    
    # controller.py (within the Controller class)

    def search_note(self, note_code) -> Note or None: # type: ignore
        """
        Search for a note by its code in the current patient's record.

        Args:
            note_code (str): The code of the note to search for.

        Returns:
            Note or None: The found note, or None if not found or if the user is not logged in or no patient is selected.
        """
        if not self.logged_in:
            #print("Please log in first.")
            raise IllegalAccessException
        if not self.current_patient:
            #print("Please select a patient first.")
            raise NoCurrentPatientException

        return self.current_patient.search_note(note_code)

    # controller.py (within the Controller class)

    def retrieve_notes(self, search_text) -> list[Note]:
        """
        Retrieve notes for the current patient that contain specific text, ordered by newest first.

        Args:
            search_text (str): The text to search for within the notes.

        Returns:
            list: A list of matching notes, ordered from newest to oldest, or None if the user is not logged in or no patient is selected.
        """
        if not self.logged_in:
            #print("Please log in first.")
            raise IllegalAccessException
        if not self.current_patient:
            #print("Please select a patient first.")
            raise NoCurrentPatientException
        if not search_text:
            #print("Please provide valid search text.")
            return None

        return self.current_patient.retrieve_notes(search_text)

    def update_note(self, note_code, new_text) -> Note or None: # type: ignore
        """
        Updates the text of a note identified by its code.

        Args:
            note_code (str): The code of the note to update.
            new_text (str): The new text to set for the note.

        Returns:
            Note or None: The updated note if successful, or None if the user is not logged in, no patient is selected, or the note is not found.
        """
        if not self.logged_in:
            #print("Please login and select a patient first")
            raise IllegalAccessException
        
        if not self.current_patient:
            raise NoCurrentPatientException

        return self.current_patient.update_note(note_code,new_text)

    def delete_note(self,note_code) -> bool:
        """
        Deletes a note identified by its code from the current patient's record.

        Args:
            note_code (str): The code of the note to delete.

        Returns:
            bool: True if the note was deleted successfully, False if the user is not logged in, no patient is selected, or the note is not found.
        """
        if not self.logged_in:
            #print("Login and select a patient first.")
            raise IllegalAccessException
        
        if not self.current_patient:
            raise NoCurrentPatientException

        return self.current_patient.delete_note(note_code)
            
    def list_notes(self) -> list[Note]:
        """
        Lists all notes for the currently selected patient.

        Returns:
            list or None: A list of notes for the current patient, or None if the user is not logged in or no patient is selected.
        """
        if not self.logged_in :
            #print("Login and select a patient first.")
            raise IllegalAccessException

        if not self.current_patient:
            raise NoCurrentPatientException

        return self.current_patient.list_notes()
    
    def load_users(self):
        with open("clinic/users.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                username = data[0]
                hashed_password = data[1]
                self.users[username] = hashed_password

    def log_change(self, change_description):
        """Add a change to the session log."""
        self.session_changes.append(change_description)

    def get_session_changes(self):
        """Retrieve the list of changes."""
        return self.session_changes
    

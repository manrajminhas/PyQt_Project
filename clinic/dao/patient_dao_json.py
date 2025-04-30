import json
from .patient_dao import PatientDAO  # Importing the abstract base class
from .patient_encoder import PatientEncoder
from .patient_decoder import PatientDecoder
import os
class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave):
        # Initialize an empty dictionary to store patients, keyed by their unique identifier (e.g., phn)
        self.patients = {}
        self.autosave = autosave
        self.filepath = "clinic/patients.json"

        loaded_patients = self.load_patients()
        if autosave and loaded_patients is not None:
            #print("load patients called")
            self.patients = loaded_patients

    def load_patients(self):
        #print("entered loading patients")

        try:
            with open("clinic/patients.json", "r") as file:
                self.patients = json.load(file, cls=PatientDecoder)
                #print("patients loaded")
                #print(self.patients)
                #print(type(self.patients))
        except FileNotFoundError:
            return {}

    def save_patients(self):
        if self.autosave:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            #print(f"Saving {len(self.patients)} patients to {self.filepath}")
            #print("Saving to:", os.path.abspath(self.filepath))

            with open(self.filepath, "w") as file:
                json.dump(self.patients, file, cls=PatientEncoder)
                #print("file saved successfully")
                
    #done 
    def search_patient(self, key):
        """Searches for a patient by a specific key (e.g., phn)."""
        #print("search ",self.patients.get(key))
        return self.patients.get(key)

    #done
    def create_patient(self, patient):
        """Adds a new patient to the in-memory collection."""
        
        self.patients[patient.phn] = patient
            
        if self.autosave:  # Save to file if autosave is enabled
            #print("patients saved in create")
            self.save_patients()

    #done
    def retrieve_patients(self, search_string):
        """Retrieves all patients that match a given search string."""
        # Assuming search_string might match with part of the patient's data, such as name
        matching_patients = [
            patient for patient in self.patients.values()
            if search_string.lower() in patient.name.lower()
        ]

        if not matching_patients:
            return []
        
        return matching_patients

    #done
    def update_patient(self, phn, updated_patient):
        """Updates an existing patient's information based on a key."""
        if phn in self.patients:
            self.patients[phn] = updated_patient

        if self.autosave:  # Save to file if autosave is enabled
            #print("patients saved in update")
            
            self.save_patients()


            
    #done
    def delete_patient(self, key):
        """Deletes a patient from the collection by their key."""
        
        #print("trying to delete phn: ",key)
        #print("these are the patients:",self.patients)
        if key in self.patients:
            #print("entered deletion if statement")
            del self.patients[key]

        if self.autosave:  # Save to file if autosave is enabled
            #print("patients saved in delete")
            #print("after deletion",self.patients)
            self.save_patients()


    #done
    def list_patients(self):
        """Lists all patients currently stored."""
        return list(self.patients.values())

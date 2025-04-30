# clinic/dao/note_dao_pickle.py
import datetime
import pickle
import os
from .note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    def __init__(self,phn,autosave:bool):
        self.notes = []  # Array to store notes 
        
        if not autosave:
            self.autocounter = 1  # autocounter to assign unique IDs to notes
        
        self.autosave = autosave
        self.phn = phn

        self.filepath = f'clinic/records/{self.phn}.dat'
        if self.autosave:
            #print("load notes called")
            self._load_notes()

    def _load_notes(self):
        """Loads notes from a file for a specific patient (phn)."""
        #print("loading notes for ",self.phn)
        
        try:
            with open(self.filepath, 'rb') as file:
                data = pickle.load(file)
                self.notes = data.get('notes',[])
                # Update autocounter based on the latest note
                if self.notes:
                    self.autocounter = max(note.code for note in self.notes)+1 if self.notes else 1
        except FileNotFoundError:
            self.notes = []
            self.autocounter = 1

        #print(f"Loaded {len(self.notes)} notes. Autocounter set to {self.autocounter}")


    def _save_notes(self):
        """Saves notes to a file for a specific patient (phn)."""
        
        if not self.autosave:
            return

        #print("saving notes in ",self.phn)
        #print("notes are: ")
        #for note in self.notes:
            #print(note)

        if not os.path.exists("clinic/records"):
    # Create the directory
            os.makedirs("clinic/records")

        with open(self.filepath, 'wb') as file:
            data = {'notes': self.notes}
            pickle.dump(data, file)

    def create_note(self, text):
        """Creates a new note, assigns it a unique ID, and stores it in the collection."""
        #print("entered create note in note dao pickle")
		
        
        current_time = datetime.datetime.now()
        new_note = Note(self.autocounter,text,current_time)
        self.notes.append(new_note)
        self.autocounter += 1
        #print("autocounter value is: ",self.autocounter)

        #print(f"Created note with code {new_note.code}. Autocounter updated to {self.autocounter}")


        if self.autosave:
            self._save_notes()
        
        return new_note
		
    def search_note(self, code):
        """Finds a note by its ID (key) if it exists."""
        note = next((note for note in self.notes if note.code == code), None)
        return note

    def retrieve_notes(self, search_string):
        """Retrieves notes that contain the search string in their text."""
        retrieved_notes = []

        for note in self.notes:
            if search_string in note.text:
                retrieved_notes.append(note)
        
        return retrieved_notes
    
    
    def update_note(self, key, text):
        """Updates the text of an existing note by its ID."""
        updated_note = None
        for note in self.notes:
            if note.code == key:
                updated_note = note
                break

        if not updated_note:
            return False

        updated_note.text = text
        updated_note.timestamp = datetime.datetime.now()

        if self.autosave:
            self._save_notes()
        
        return True

    def delete_note(self,note_code):

        original_count = len(self.notes)
        self.notes = [note for note in self.notes if note.code != note_code]

        if self.autosave:
            self._save_notes()
        
        if len(self.notes) < original_count:
            #print(f"Note {note_code} deleted successfully")
            return True
        
        else: 
            #print("Note not found")
            return False
        
        
        
    def list_notes(self):
        """Returns a list of all notes."""
        
        notes_list = []

        for i in range(-1,-len(self.notes)-1,-1):
            notes_list.append(self.notes[i])

        return notes_list
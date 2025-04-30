# clinic/note.py
from datetime import datetime

class Note:
    """
    Represents a note associated with a patient.

    Attributes:
        code (str): The unique identifier for the note.
        text (str): The content of the note.
        timestamp (datetime): The time when the note was created or last updated.
    """
    def __init__(self, code, text, timestamp=None):
        """
        Initializes a new note with a specified code, text, and optional timestamp.

        Args:
            code (str): The unique code for the note.
            text (str): The content of the note.
            timestamp (datetime, optional): The time of note creation. 
                                             Defaults to the current time if not provided.
        """
        self.code = code
        self.text = text
        self.timestamp = timestamp or datetime.now()

    def update_text(self, new_text):
        """
        Updates the text content of the note and resets the timestamp to the current time.

        Args:
            new_text (str): The new content to be set for the note.
        """
        self.text = new_text
        self.timestamp = datetime.now()
    
    # note.py
    def __eq__(self, other):
        """
        Checks if two Note objects are equal based on their attributes.

        Args:
            other (Note): The other Note object to compare with.

        Returns:
            bool: True if both notes have the same code and text; otherwise, False.
        """

        return (
            isinstance(other, Note) and
            self.code == other.code and
            self.text == other.text 
            #and self.timestamp == other.timestamp
        )

    def __str__(self):
        """
        Returns a string representation of the Note object.

        Returns:
            str: A string describing the note, including its code, text, and timestamp.
        """
        return f"Note {self.code}: {self.text} (Timestamp: {self.timestamp})"

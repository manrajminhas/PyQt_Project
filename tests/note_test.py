# note_test.py

import unittest
from clinic.note import Note
from datetime import datetime

class TestNoteEquality(unittest.TestCase):
    
    def setUp(self):
        # Common timestamp for easier comparison
        self.timestamp = datetime(2024, 10, 27, 10, 30)
    
    def test_identical_notes(self):
        note1 = Note(1, "Patient has a headache.", self.timestamp)
        note2 = Note(1, "Patient has a headache.", self.timestamp)
        self.assertEqual(note1, note2, "Identical notes should be equal")

    def test_different_codes(self):
        note1 = Note(1, "Patient has a headache.", self.timestamp)
        note2 = Note(2, "Patient has a headache.", self.timestamp)
        self.assertNotEqual(note1, note2, "Notes with different codes should not be equal")
        
    def test_different_text(self):
        note1 = Note(1, "Patient has a headache.", self.timestamp)
        note2 = Note(1, "Patient has a mild headache.", self.timestamp)
        self.assertNotEqual(note1, note2, "Notes with different text should not be equal")
        
    def test_non_note_comparison(self):
        note1 = Note(1, "Patient has a headache.", self.timestamp)
        self.assertNotEqual(note1, "Some string", "Comparing Note to a non-Note object should return False")

if __name__ == "__main__":
    unittest.main()

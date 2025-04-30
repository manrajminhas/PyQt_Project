import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from clinic.note import Note
from clinic.patient_record import PatientRecord


class TestPatientRecord(unittest.TestCase):

    def setUp(self):
        # Mock NoteDAOPickle and patch it in PatientRecord
        self.mock_note_dao = MagicMock()
        with patch('clinic.patient_record.NoteDAOPickle', return_value=self.mock_note_dao):
            self.phn = "123456789"
            self.autosave = False
            self.record = PatientRecord(self.phn, self.autosave)

    def test_add_note(self):
        # Mock the create_note method to return a simulated Note object
        mock_note = Note(code=1, text="Patient has a mild headache.", timestamp=datetime.now())
        self.mock_note_dao.create_note.return_value = mock_note

        # Call create_note and verify the behavior
        note = self.record.create_note("Patient has a mild headache.")
        self.mock_note_dao.create_note.assert_called_once_with("Patient has a mild headache.")
        self.assertEqual(note.text, "Patient has a mild headache.")
        self.assertEqual(note.code, 1)

    def test_add_multiple_notes(self):
        # Mock create_note for multiple calls
        mock_notes = [
            Note(code=1, text="Patient complains of nausea.", timestamp=datetime.now()),
            Note(code=2, text="Patient reports dizziness.", timestamp=datetime.now()),
            Note(code=3, text="Patient shows improvement.", timestamp=datetime.now()),
        ]
        self.mock_note_dao.create_note.side_effect = mock_notes

        # Add multiple notes
        note1 = self.record.create_note("Patient complains of nausea.")
        note2 = self.record.create_note("Patient reports dizziness.")
        note3 = self.record.create_note("Patient shows improvement.")

        # Verify the mock calls and note properties
        self.assertEqual(note1.code, 1)
        self.assertEqual(note2.code, 2)
        self.assertEqual(note3.code, 3)
        self.mock_note_dao.create_note.assert_has_calls([
            unittest.mock.call("Patient complains of nausea."),
            unittest.mock.call("Patient reports dizziness."),
            unittest.mock.call("Patient shows improvement."),
        ])

    def test_get_all_notes(self):
        # Mock list_notes to return a simulated list of notes
        mock_notes = [
            Note(code=1, text="Patient shows high blood pressure.", timestamp=datetime.now()),
            Note(code=2, text="Patient reports no headaches.", timestamp=datetime.now()),
        ]
        self.mock_note_dao.list_notes.return_value = mock_notes

        # Retrieve notes and verify the order
        notes = self.record.list_notes()
        self.mock_note_dao.list_notes.assert_called_once()
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, "Patient shows high blood pressure.")
        self.assertEqual(notes[1].text, "Patient reports no headaches.")

    def test_get_all_notes_empty(self):
        # Mock list_notes to return an empty list
        self.mock_note_dao.list_notes.return_value = []

        # Retrieve notes and verify behavior
        notes = self.record.list_notes()
        self.mock_note_dao.list_notes.assert_called_once()
        self.assertEqual(len(notes), 0)

    def test_update_note(self):
        # Mock update_note to return an updated Note object
        mock_updated_note = Note(code=1, text="Updated note text.", timestamp=datetime.now())
        self.mock_note_dao.update_note.return_value = mock_updated_note

        # Call update_note and verify behavior
        updated_note = self.record.update_note(1, "Updated note text.")
        self.mock_note_dao.update_note.assert_called_once_with(1, "Updated note text.")
        self.assertEqual(updated_note.code, 1)
        self.assertEqual(updated_note.text, "Updated note text.")

    def test_delete_note_success(self):
        # Mock delete_note to return True (indicating successful deletion)
        self.mock_note_dao.delete_note.return_value = True

        # Call delete_note and verify behavior
        result = self.record.delete_note(1)
        self.mock_note_dao.delete_note.assert_called_once_with(1)
        self.assertTrue(result)

    def test_delete_note_failure(self):
        # Mock delete_note to return False (indicating deletion failed)
        self.mock_note_dao.delete_note.return_value = False

        # Call delete_note and verify behavior
        result = self.record.delete_note(999)  # Assume 999 is a nonexistent note code
        self.mock_note_dao.delete_note.assert_called_once_with(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

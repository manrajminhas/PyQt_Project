# patient_test.py

import unittest
from clinic.patient import Patient
from datetime import datetime

class TestPatient(unittest.TestCase):

    def setUp(self):
        # Common attributes for testing
        self.phn = 123456789
        self.name = "John Doe"
        self.birth_date = "1990-01-01"
        self.phone = "250-555-1234"
        self.email = "johndoe@example.com"
        self.address = "123 Main St, Anytown"
        
        # Initialize a Patient instance
        self.patient = Patient(
            phn=self.phn,
            name=self.name,
            birth_date=self.birth_date,
            phone=self.phone,
            email=self.email,
            address=self.address
        )

    def test_patient_initialization(self):
        """Test that a patient is initialized with the correct data."""
        self.assertEqual(self.patient.phn, self.phn)
        self.assertEqual(self.patient.name, self.name)
        self.assertEqual(self.patient.birth_date, self.birth_date)
        self.assertEqual(self.patient.phone, self.phone)
        self.assertEqual(self.patient.email, self.email)
        self.assertEqual(self.patient.address, self.address)

    def test_patient_equality(self):
        """Test the equality method for patients with identical data."""
        patient_clone = Patient(
            phn=self.phn,
            name=self.name,
            birth_date=self.birth_date,
            phone=self.phone,
            email=self.email,
            address=self.address
        )
        self.assertEqual(self.patient, patient_clone, "Patients with identical data should be equal")

    def test_patient_inequality_phn(self):
        """Test that patients with different PHNs are not equal."""
        different_patient = Patient(
            phn=987654321,
            name=self.name,
            birth_date=self.birth_date,
            phone=self.phone,
            email=self.email,
            address=self.address
        )
        self.assertNotEqual(self.patient, different_patient, "Patients with different PHNs should not be equal")

    def test_patient_inequality_other_fields(self):
        """Test that patients with different names, birth_dates, phones, emails, or addresses are not equal."""
        # Different name
        different_name_patient = Patient(
            phn=self.phn,
            name="Jane Doe",
            birth_date=self.birth_date,
            phone=self.phone,
            email=self.email,
            address=self.address
        )
        self.assertNotEqual(self.patient, different_name_patient, "Patients with different names should not be equal")
        
        # Different birth date
        different_birth_date_patient = Patient(
            phn=self.phn,
            name=self.name,
            birth_date="2000-01-01",
            phone=self.phone,
            email=self.email,
            address=self.address
        )
        self.assertNotEqual(self.patient, different_birth_date_patient, "Patients with different birth dates should not be equal")
        
        # Different phone
        different_phone_patient = Patient(
            phn=self.phn,
            name=self.name,
            birth_date=self.birth_date,
            phone="250-555-5678",
            email=self.email,
            address=self.address
        )
        self.assertNotEqual(self.patient, different_phone_patient, "Patients with different phone numbers should not be equal")
        
        # Different email
        different_email_patient = Patient(
            phn=self.phn,
            name=self.name,
            birth_date=self.birth_date,
            phone=self.phone,
            email="janedoe@example.com",
            address=self.address
        )
        self.assertNotEqual(self.patient, different_email_patient, "Patients with different emails should not be equal")
        
        # Different address
        different_address_patient = Patient(
            phn=self.phn,
            name=self.name,
            birth_date=self.birth_date,
            phone=self.phone,
            email=self.email,
            address="456 Other St, Othercity"
        )
        self.assertNotEqual(self.patient, different_address_patient, "Patients with different addresses should not be equal")

if __name__ == "__main__":
    unittest.main()

import json

class PatientDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        # Convert all keys to integers if possible
        int_keyed_dict = {}
        for key, value in dct.items():
            try:
                # Attempt to convert key to integer
                int_key = int(key)
            except (ValueError, TypeError):
                # If not convertible, keep the original key
                int_key = key
            int_keyed_dict[int_key] = value
        
        # Import Patient here to avoid circular import issues
        from clinic.patient import Patient
        from clinic.patient_record import PatientRecord
        from clinic.note import Note
        
        # Check if dictionary contains Patient attributes
        if "phn" in int_keyed_dict and "name" in int_keyed_dict:
            records = int_keyed_dict.get("records", [])
            # Create PatientRecord objects for each record
            patient_records = []
            for record in records:
                patient_record = PatientRecord()
                patient_record.note_dao.notes = [Note(**note) for note in record.get("notes", [])]
                patient_records.append(patient_record)
            
            # Convert dictionary to Patient object
            return Patient(
                phn=int_keyed_dict["phn"],
                name=int_keyed_dict["name"],
                birth_date=int_keyed_dict.get("birth_date"),  # Handle optional attributes safely
                phone=int_keyed_dict.get("phone_number"),  # Handle optional attributes safely
                email=int_keyed_dict.get("email"),  # Handle optional attributes safely
                address=int_keyed_dict.get("address"),  # Handle optional attributes safely
                autosave = True
                # Map other attributes if needed
            )
        return int_keyed_dict  # Return the modified dictionary

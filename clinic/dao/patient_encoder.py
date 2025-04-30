import json

class PatientEncoder(json.JSONEncoder):
    def default(self, obj):
        # Import Patient here to avoid circular import issues
        from clinic.patient import Patient
        from clinic.patient_record import PatientRecord

        if isinstance(obj, Patient):
            # Convert Patient object to a dictionary
            return {
                "phn": obj.phn,
                "name": obj.name,
                "birth_date": obj.birth_date,
                "phone_number": obj.phone,
                "email": obj.email,
                "address": obj.address,
                "record": obj.record
                    
                
            }
        
        elif isinstance(obj, PatientRecord):
            # Serialize notes using the note_dao's `notes` attribute
            return {
                "notes": [note.__dict__ for note in obj.note_dao.notes],
            }
        
        # Let the base class handle other object types
        return super().default(obj)

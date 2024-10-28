
# This is a simple database service that stores patient information in a dictionary.
class PatientDbService:
    def __init__(self) -> None:
        self.db = {
            "John Doe": {
                "patient_id":"123456",
                "first_name": "John",
                "last_name": "Doe",
                "status": "alive",
                "birth_date": "1976-01-01",
                "age": 42,                
                "history": {
                    "allergies": ["penicillin"],
                    "medications": ["aspirin, ibuprofen"],
                },
            },
            "Jane Doe": {
                "patient_id":"123457",
                "first_name": "Jane",
                "last_name": "Doe",
                "status": "alive",
                "birth_date": "1986-01-01",
                "age": 35,
                "history": {
                    "allergies": ["peanuts"],
                    "medications": ["insulin"],
                },
            },
            "Jim Doe": {
                "patient_id":"123458",
                "first_name": "Jim",
                "last_name": "Doe",
                "status": "deceased",
                "birth_date": "1956-01-01",
                "age": 65,
                "history": {
                    "allergies": ["none"],
                    "medications": ["none"],
                },
            },
            "Jill Doe": {
                "patient_id":"123459",
                "first_name": "Jill",
                "last_name": "Doe",
                "status": "alive",
                "birth_date": "1996-01-01",
                "age": 25,
                "history": {
                    "allergies": ["none"],
                    "medications": ["none"],
                },
            },
            "Jack Doe": {
                "patient_id":"123460",
                "first_name": "Jack",
                "last_name": "Doe",
                "status": "alive",
                "birth_date": "1986-01-02",
                "age": 35,
                "history": {
                    "allergies": ["none"],
                    "medications": ["none"],
                },
            },
        }
            
    def get_patient_info_by_id(self, patient_id: str) -> dict:
        """
        Call this function to lookup the patient's personal information in the internal database.
        """
        for patient in self.db.values():
            if patient["patient_id"] == patient_id:
                return patient
        
        # throw an error if the patient_id is not found
        raise ValueError(f"Patient with id {patient_id} not found.")
    
    def lookup_patient_info(self, first_name: str, last_name: str) -> dict:
        """
        Call this function to lookup the patient's personal information in the internal database.
        """
        full_name = f"{first_name} {last_name}"
        if full_name in self.db:
            return self.db[full_name]
        else:
            return {
                "first_name": first_name,
                "last_name": last_name,
                "status": "not found",
            }
        
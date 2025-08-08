import requests
import json
import os
import random

# Public HAPI FHIR server base URL
FHIR_BASE = "https://hapi.fhir.org/baseR4"

def fetch_random_patient_data():
    try:
        print("🔍 Fetching random patient data from HAPI FHIR server...")
        
        # Fetch a larger sample to randomize from
        patient_url = f"{FHIR_BASE}/Patient?_count=50"
        resp = requests.get(patient_url, timeout=10)
        patient_bundle = resp.json()

        if 'entry' in patient_bundle and len(patient_bundle['entry']) > 0:
            # Randomly select a patient
            random_patient_entry = random.choice(patient_bundle['entry'])
            patient = random_patient_entry['resource']
            
            print("✅ Live Random Patient Data from HAPI FHIR Server")
            print("=" * 50)
            print("Patient Demographics:")
            print(json.dumps(patient, indent=2))

            # Fetch Observations for this specific patient
            patient_id = patient['id']
            obs_url = f"{FHIR_BASE}/Observation?patient={patient_id}&_count=5"
            obs_resp = requests.get(obs_url, timeout=10)
            obs_bundle = obs_resp.json()

            observations = obs_bundle.get('entry', [])
            if observations:
                print(f"\nClinical Observations for Patient {patient_id}:")
                for i, entry in enumerate(observations, 1):
                    obs = entry['resource']
                    print(f"\n--- Observation {i} ---")
                    print(json.dumps(obs, indent=2))
            else:
                print(f"\nNo observations found for patient {patient_id}")
                # Try to get some general observations as examples
                print("Fetching general observations as examples...")
                general_obs_url = f"{FHIR_BASE}/Observation?_count=3"
                general_obs_resp = requests.get(general_obs_url, timeout=10)
                general_obs_bundle = general_obs_resp.json()
                general_observations = general_obs_bundle.get('entry', [])
                
                if general_observations:
                    print("\nExample Clinical Observations from FHIR Server:")
                    for i, entry in enumerate(general_observations, 1):
                        obs = entry['resource']
                        print(f"\n--- Example Observation {i} ---")
                        print(json.dumps(obs, indent=2))
            
            return True
        else:
            print("No patients found in FHIR server response")
            return False
            
    except Exception as e:
        print(f"❌ Error fetching from FHIR server: {e}")
        return False

def load_sample_data():
    print("📁 Loading fallback sample data from examples folder...")
    print("=" * 50)
    
    # Load and print sample patient
    sample_patient_path = os.path.join(os.path.dirname(__file__), '../examples/sample_patient.json')
    with open(sample_patient_path, 'r') as f:
        sample_patient = json.load(f)
    print("Patient Demographics (Sample):")
    print(json.dumps(sample_patient, indent=2))
    
    # Load and print sample observation
    sample_obs_path = os.path.join(os.path.dirname(__file__), '../examples/sample_observation.json')
    with open(sample_obs_path, 'r') as f:
        sample_obs = json.load(f)
    print("\nSample Lab Result (Observation):")
    print(json.dumps(sample_obs, indent=2))

# Main execution
if __name__ == "__main__":
    print("🏥 FHIR API Integration Demo - Random Patient Fetcher")
    print("=" * 60)
    
    success = fetch_random_patient_data()
    
    if not success:
        print("\n" + "=" * 60)
        print("Falling back to sample data...")
        load_sample_data()
    
    print("\n" + "=" * 60)
    print("Demo completed! 🎉") 
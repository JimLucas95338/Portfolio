import requests
import json
import os

# Public HAPI FHIR server base URL
FHIR_BASE = "https://hapi.fhir.org/baseR4"

# Fetch a Patient resource (first available)
patient_url = f"{FHIR_BASE}/Patient?_count=1"
resp = requests.get(patient_url)
patient_bundle = resp.json()

if 'entry' in patient_bundle and len(patient_bundle['entry']) > 0:
    patient = patient_bundle['entry'][0]['resource']
    print("Patient Demographics:")
    print(json.dumps(patient, indent=2))

    # Fetch Observations (e.g., lab results) for the patient
    patient_id = patient['id']
    obs_url = f"{FHIR_BASE}/Observation?patient={patient_id}&_count=3"
    obs_resp = requests.get(obs_url)
    obs_bundle = obs_resp.json()

    print("\nSample Lab Results (Observations):")
    for entry in obs_bundle.get('entry', []):
        obs = entry['resource']
        print(json.dumps(obs, indent=2))
else:
    print("No Patient resources found in the FHIR server response.\nDisplaying sample data from examples folder.\n")
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
import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import os

FHIR_BASE = "https://hapi.fhir.org/baseR4"
SAMPLE_PATIENT_PATH = os.path.join(os.path.dirname(__file__), '../examples/sample_patient.json')
SAMPLE_OBS_PATH = os.path.join(os.path.dirname(__file__), '../examples/sample_observation.json')

def fetch_patient_and_obs():
    try:
        patient_url = f"{FHIR_BASE}/Patient?_count=1"
        resp = requests.get(patient_url, timeout=10)
        patient_bundle = resp.json()
        if 'entry' in patient_bundle and len(patient_bundle['entry']) > 0:
            patient = patient_bundle['entry'][0]['resource']
            patient_id = patient['id']
            obs_url = f"{FHIR_BASE}/Observation?patient={patient_id}&_count=3"
            obs_resp = requests.get(obs_url, timeout=10)
            obs_bundle = obs_resp.json()
            observations = [entry['resource'] for entry in obs_bundle.get('entry', [])]
            return patient, observations, False
    except Exception as e:
        print(f"Error fetching from FHIR server: {e}")
    with open(SAMPLE_PATIENT_PATH, 'r') as f:
        patient = json.load(f)
    with open(SAMPLE_OBS_PATH, 'r') as f:
        observations = [json.load(f)]
    return patient, observations, True

def format_patient_summary(patient):
    name = patient.get('name', [{}])[0]
    full_name = ' '.join(name.get('given', [])) + ' ' + name.get('family', '')
    gender = patient.get('gender', 'N/A').capitalize()
    birth = patient.get('birthDate', 'N/A')
    summary = f"Name: {full_name.strip()}\nGender: {gender}\nBirth Date: {birth}\n"
    return summary

def format_observation_summary(obs):
    code = obs.get('code', {}).get('coding', [{}])[0]
    display = code.get('display', 'N/A')
    value = obs.get('valueQuantity', {}).get('value', 'N/A')
    unit = obs.get('valueQuantity', {}).get('unit', '')
    date = obs.get('effectiveDateTime', obs.get('issued', 'N/A'))
    return f"- {display}: {value} {unit} ({date})"

def display_results():
    patient, observations, is_sample = fetch_patient_and_obs()
    # Summary tab
    summary_output.config(state='normal')
    summary_output.delete(1.0, tk.END)
    if is_sample:
        summary_output.insert(tk.END, "[Sample Data Loaded]\n\n")
    summary_output.insert(tk.END, "Patient Demographics:\n")
    summary_output.insert(tk.END, format_patient_summary(patient) + "\n")
    summary_output.insert(tk.END, "Lab Results (Observations):\n")
    for obs in observations:
        summary_output.insert(tk.END, format_observation_summary(obs) + "\n")
    summary_output.config(state='disabled')
    # Raw JSON tab
    raw_output.config(state='normal')
    raw_output.delete(1.0, tk.END)
    if is_sample:
        raw_output.insert(tk.END, "[Sample Data Loaded]\n\n")
    raw_output.insert(tk.END, "Patient Demographics (Raw JSON):\n")
    raw_output.insert(tk.END, json.dumps(patient, indent=2) + "\n\n")
    raw_output.insert(tk.END, "Lab Results (Observations, Raw JSON):\n")
    for obs in observations:
        raw_output.insert(tk.END, json.dumps(obs, indent=2) + "\n\n")
    raw_output.config(state='disabled')

# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("FHIR Patient & Lab Results Demo")
root.geometry("750x650")

frame = tk.Frame(root)
frame.pack(pady=10)

fetch_btn = tk.Button(frame, text="Fetch Random Patient", command=display_results)
fetch_btn.pack()

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

summary_output = scrolledtext.ScrolledText(notebook, width=90, height=32, state='disabled')
raw_output = scrolledtext.ScrolledText(notebook, width=90, height=32, state='disabled')

notebook.add(summary_output, text='Summary')
notebook.add(raw_output, text='Raw JSON')

root.mainloop() 
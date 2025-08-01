import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class MedicationReminderSystem:
    def __init__(self, data_file):
        """Initialize the medication reminder system."""
        self.df = pd.read_csv(data_file)
        self.df['LastTaken'] = pd.to_datetime(self.df['LastTaken'])
        self.df['NextDose'] = pd.to_datetime(self.df['NextDose'], errors='coerce')
        
    def get_upcoming_reminders(self, hours_ahead=24):
        """Get medications that need reminders in the next X hours."""
        now = datetime.now()
        future_time = now + timedelta(hours=hours_ahead)
        
        upcoming = self.df[
            (self.df['NextDose'] >= now) & 
            (self.df['NextDose'] <= future_time)
        ].copy()
        
        upcoming['HoursUntilDose'] = (upcoming['NextDose'] - now).dt.total_seconds() / 3600
        return upcoming.sort_values('HoursUntilDose')
    
    def get_missed_doses(self, hours_threshold=2):
        """Get medications that are overdue for more than X hours."""
        now = datetime.now()
        threshold_time = now - timedelta(hours=hours_threshold)
        
        missed = self.df[
            (self.df['NextDose'] < threshold_time) & 
            (self.df['AdherenceRate'] > 0)  # Only active medications
        ].copy()
        
        missed['HoursOverdue'] = (now - missed['NextDose']).dt.total_seconds() / 3600
        return missed.sort_values('HoursOverdue', ascending=False)
    
    def get_low_adherence_patients(self, threshold=80):
        """Get patients with adherence rates below threshold."""
        patient_adherence = self.df.groupby('PatientID')['AdherenceRate'].mean()
        low_adherence_patients = patient_adherence[patient_adherence < threshold]
        
        return self.df[self.df['PatientID'].isin(low_adherence_patients.index)]
    
    def get_safety_alerts(self):
        """Get patients with side effects or drug interactions."""
        safety_alerts = self.df[
            (self.df['SideEffects'] != 'None') | 
            (self.df['DrugInteractions'] != 'None')
        ].copy()
        
        return safety_alerts
    
    def mark_dose_taken(self, patient_id, medication, timestamp=None):
        """Mark a dose as taken and update next dose time."""
        if timestamp is None:
            timestamp = datetime.now()
            
        mask = (self.df['PatientID'] == patient_id) & (self.df['Medication'] == medication)
        
        if mask.any():
            self.df.loc[mask, 'LastTaken'] = timestamp
            
            # Calculate next dose based on frequency
            row = self.df[mask].iloc[0]
            next_dose = self._calculate_next_dose(row, timestamp)
            self.df.loc[mask, 'NextDose'] = next_dose
            
            return True
        return False
    
    def _calculate_next_dose(self, medication_row, current_time):
        """Calculate the next dose time based on medication frequency."""
        frequency = medication_row['Frequency']
        
        if frequency == 'Once Daily':
            return current_time + timedelta(days=1)
        elif frequency == 'Twice Daily':
            # If it's morning dose, next is evening; if evening, next is tomorrow morning
            current_hour = current_time.hour
            if current_hour < 12:  # Morning dose
                return current_time.replace(hour=20, minute=0, second=0, microsecond=0)
            else:  # Evening dose
                return (current_time + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
        elif frequency == 'As Needed':
            return None  # No scheduled next dose
        else:
            return current_time + timedelta(days=1)  # Default to daily
    
    def generate_daily_report(self):
        """Generate a daily summary report."""
        now = datetime.now()
        
        report = {
            'date': now.strftime('%Y-%m-%d'),
            'total_patients': self.df['PatientID'].nunique(),
            'total_medications': len(self.df),
            'upcoming_reminders': len(self.get_upcoming_reminders()),
            'missed_doses': len(self.get_missed_doses()),
            'low_adherence_patients': len(self.get_low_adherence_patients()),
            'safety_alerts': len(self.get_safety_alerts()),
            'average_adherence': self.df['AdherenceRate'].mean()
        }
        
        return report
    
    def get_patient_summary(self, patient_id):
        """Get a summary for a specific patient."""
        patient_data = self.df[self.df['PatientID'] == patient_id]
        
        if patient_data.empty:
            return None
            
        summary = {
            'patient_id': patient_id,
            'name': patient_data.iloc[0]['Name'],
            'age': patient_data.iloc[0]['Age'],
            'primary_condition': patient_data.iloc[0]['PrimaryCondition'],
            'medications': len(patient_data),
            'average_adherence': patient_data['AdherenceRate'].mean(),
            'upcoming_doses': len(self.get_upcoming_reminders().query(f'PatientID == {patient_id}')),
            'missed_doses': len(self.get_missed_doses().query(f'PatientID == {patient_id}')),
            'safety_alerts': len(self.get_safety_alerts().query(f'PatientID == {patient_id}'))
        }
        
        return summary 
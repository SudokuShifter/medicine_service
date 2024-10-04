from django import forms

from .models import PatientRecord


class RecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['appointment_date', 'description_patient', 'description']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
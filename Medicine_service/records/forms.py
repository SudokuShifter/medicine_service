from django import forms

from .models import PatientRecord


class RecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['description_patient', 'description']

from django import forms

from .models import PatientRecord


class RecordForm(forms.ModelForm):
    """
    Форма для записи пациента к врачу. Наслудется от forms.ModelForm (базовая штука джанги)
    Класс Meta внутри сделан для удобства.
    """
    class Meta:
        model = PatientRecord
        fields = ['appointment_date', 'description_patient', 'description']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
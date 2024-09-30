from django import forms

from .models import ScheduleDoctor


class CreateScheduleDoctor(forms.ModelForm):
    class Meta:
        model = ScheduleDoctor
        fields = [
            'start_at', 'end_at'
        ]
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'type': 'datetime'}),
            'end_at': forms.DateTimeInput(attrs={'type': 'datetime'}),
        }



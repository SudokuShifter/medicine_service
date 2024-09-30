from django.shortcuts import render
from django.views.generic import CreateView

from .models import ScheduleDoctor
from .forms import CreateScheduleDoctor
# Create your views here.


class CreateSchedule(CreateView):
    model = ScheduleDoctor
    form_class = CreateScheduleDoctor
    # template_name =

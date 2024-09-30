from django.shortcuts import render
from django.views.generic import CreateView


def doctors_view(request):
    return render(request, 'doctors.html')
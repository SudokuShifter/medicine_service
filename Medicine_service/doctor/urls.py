from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.DoctorHome.as_view(), name='home'),
]
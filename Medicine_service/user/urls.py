from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.UserHome.as_view(), name='home'),
]
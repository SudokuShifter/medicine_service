from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.doctors_view, name='doc_list')
]

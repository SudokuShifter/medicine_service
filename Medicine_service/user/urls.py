from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.UserHome.as_view(), name='home'),
    path('lk/<slug:patient_slug>', views.UserLk.as_view(), name='lk'),

]
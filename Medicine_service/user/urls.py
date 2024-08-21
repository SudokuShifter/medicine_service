from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.UserHome.as_view(), name='home'),
    path('profile/<slug:slug>', views.UserProfileView.as_view(), name='profile'),

]
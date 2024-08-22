from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('logout/', views.Logout.as_view(), name='logout')
]
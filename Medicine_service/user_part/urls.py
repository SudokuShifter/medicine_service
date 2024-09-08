from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('profile/<slug:slug>', views.UserLk.as_view(), name='lk'),
    path('profile/edit_data/', views.UserProfileCreateView.as_view(), name='first_create')
]

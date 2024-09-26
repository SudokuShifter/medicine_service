from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('register/2step', views.UserProfileCreateView.as_view(), name='register_profile'),
    path('register/3step', views.UserAddressCreateView.as_view(), name='register_address'),
    path('profile/<slug:slug>', views.UserLk.as_view(), name='lk'),
    path('profile/edit_data/', views.UserProfileCreateView.as_view(), name='edit_data')
]

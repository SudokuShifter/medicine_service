from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doc_list'),
    path('rate_doc/<int:pk>/', views.RateDoctorView.as_view(), name='rate_doc'),
    path('create/<int:pk>/', views.CreateRecord.as_view(), name='record_doc'),
    path('my_records/', views.CheckRecords.as_view(), name='check_records')
]

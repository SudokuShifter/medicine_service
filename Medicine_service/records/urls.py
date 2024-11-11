from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doc_list'),
    path('rate_doc/<int:pk>/', views.RateDoctorView.as_view(), name='rate_doc'),
    path('create_rec/<int:pk>/', views.CreateRecord.as_view(), name='record_doc'),
    path('my_records/', views.CheckRecords.as_view(), name='check_records'),
    path('update_rec/<int:pk>', views.UpdateRecord.as_view(), name='update_record'),
    path('delete_rec/<int:pk>', views.DeleteRecord.as_view(), name='delete_record'),
]

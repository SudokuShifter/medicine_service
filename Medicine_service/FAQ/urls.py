from django.urls import path
from . import views


urlpatterns = [
    path('', views.QuestionView.as_view(), name='faq_main'),
    path('add_question/', views.QuestionCreateView.as_view(), name='add_question'),
    path('my_questions/', views.QuestionAuthorListView.as_view(), name='my_questions')
]

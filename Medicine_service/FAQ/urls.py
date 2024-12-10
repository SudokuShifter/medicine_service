from django.urls import path
from . import views


urlpatterns = [
    path('', views.QuestionView.as_view(), name='faq_main'),
    path('add_question/', views.QuestionCreateView.as_view(), name='add_question'),
    path('my_questions/', views.QuestionAuthorListView.as_view(), name='my_questions'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='detail_question'),
    path('question/<int:pk>/answer/', views.AnswerQuestion.as_view(), name='answer_question'),
    path('question/<int:pk>/delete/', views.DeleteQuestion.as_view(), name='delete_question'),
]

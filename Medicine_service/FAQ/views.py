from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .models import Question
from .forms import AddQuestionForm

# Create your views here.


class QuestionView(ListView):
    paginate_by = 10
    model = Question
    template_name = 'FAQ_main.html'
    context_object_name = 'questions'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('created_at')


class QuestionAuthorListView(ListView):
    paginate_by = 10
    model = Question
    template_name = 'FAQ_author_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(patient=self.request.user.user_profile).order_by('created_at')


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'FAQ_form.html'
    form_class = AddQuestionForm
    success_url = reverse_lazy('faq_main')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.patient = self.request.user.user_profile
        question.save()
        return super().form_valid(form)

    def check_author_question(self):
        question = Question.objects.get(patient=self.request.user.user_profile)
        pass


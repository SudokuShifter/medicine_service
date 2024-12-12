from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Question, Answer
from .forms import AddQuestionForm, AnswerForm

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


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'FAQ_view.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            context['answer'] = self.object.answer
        except Answer.DoesNotExist:
            context['answer'] = None
        return context


class AnswerQuestion(CreateView):
    model = Answer
    template_name = 'FAQ_answer_form.html'
    form_class = AnswerForm
    success_url = reverse_lazy('faq_main')


    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.question = Question.objects.get(pk=self.kwargs['pk'])
        answer.doctor = self.request.user.doctor_profile
        answer.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])
        return context


class DeleteQuestion(DeleteView):
    model = Question
    success_url = reverse_lazy('faq_main')
    template_name = 'FAQ_delete_popup.html'
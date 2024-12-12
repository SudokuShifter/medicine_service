from django import forms

from .models import Question, Category, Answer


class AddQuestionForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Question
        fields = ['name', 'description', 'category']

    def save(self, commit=True):
        question = super().save(commit=False)
        question.category = self.cleaned_data['category']
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']


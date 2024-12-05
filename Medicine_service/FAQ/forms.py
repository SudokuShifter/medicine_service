from django import forms

from .models import Question, Category


class AddQuestionForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Question
        fields = ['name', 'description', 'category']

    def save(self, commit=True):
        question = super().save(commit=False)
        question.category = self.cleaned_data['category']
        return question

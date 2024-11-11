from django import forms

from .models import Question, Category


class AddQuestionForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Question
        fields = '__all__'

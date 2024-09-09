from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import CustomCreateUserForm, CustomUpdateUserForm
from .models import UserProfile
from .logic import calculate_age
# Create your views here.


def home(request):
    return render(request, 'user_part/home.html')


class UserLoginView(LoginView):
    template_name = 'user_part/login_form.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            user_profile = getattr(user, 'user_profile', None)
            if user_profile and user_profile.name:
                return reverse_lazy('lk', kwargs={'slug': user_profile.slug})
            return reverse_lazy('first_create')
        return reverse_lazy('login')


class UserCreateView(CreateView):
    model = User
    template_name = 'user_part/register_form.html'
    form_class = CustomCreateUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class UserLk(DetailView):
    model = UserProfile
    template_name = 'user_part/lk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['age'] = calculate_age(self.request.user.user_profile.birthday)
        return context


class UserProfileCreateView(CreateView):
    model = UserProfile
    template_name = 'user_part/edit_data.html'
    form_class = CustomUpdateUserForm

    def form_valid(self, form):
        # Сначала сохраняем профиль пользователя
        user_profile = form.save(commit=False)
        user = self.request.user
        user_profile.user = user
        user_profile.slug = user.username
        user_profile.save()
        # После успешного создания профиля, переходим по URL
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lk', kwargs={'slug': self.object.slug})

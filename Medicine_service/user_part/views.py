from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import CustomCreateUserForm, CustomUpdateUserForm
from .models import UserProfile, PatientStory
from .logic import calculate_age
# Create your views here.


def home(request):
    return render(request, 'user_part/home.html')


class UserLoginView(LoginView):
    """
    Класс UserLoginView наследуется от LoginView.
    В кач-ве атрибутов класса обозначена ссылка на темплейт и переопределён метод get_succes_url.
    Проверяем юзера на то имеет ли юзер данные профиля, и если не имеет, то редиректим его на заполнение.
    Если имеет данные, то в лк через slug
    """
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
    """
    Класс UserCreateView наследуется от CreateView.
    Отвечает за регистрацию пользователя
    """
    model = User
    template_name = 'user_part/register_form.html'
    form_class = CustomCreateUserForm
    success_url = reverse_lazy('login')


class UserLk(DetailView):
    """
    Класс UserLk наследуется от DetailView.
    Через метод get_object мы получаем объект модели UserProfile и используем данные в get_context_data.
    """
    model = UserProfile
    template_name = 'user_part/lk.html'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = self.get_object()
        context['user_data'] = user_data
        context['records'] = user_data.records
        context['age'] = calculate_age(user_data.birthday)
        return context


class UserProfileCreateView(CreateView):
    """
    Класс UserProfileCreateView наследуется от CreateView.
    Класс отвечает за создание/редактирование данных юзера (UserProfile).
    В методе form_valid автоматически заполняется slug и производится связка с моделью User
    """
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

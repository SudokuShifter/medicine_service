from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import CustomCreateUserForm, CustomUpdateUserForm, CustomUpdateUserAddressForm, CustomUpdateDoctorForm
from .models import UserProfile, Address, DoctorProfile
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
            user_profile = getattr(user, 'doctor_profile' if user.is_staff else 'user_profile', None)
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
    success_url = reverse_lazy('register_profile')

    def form_valid(self, form):
        # Сначала сохраняем пользователя
        response = super().form_valid(form)
        # После успешного создания пользователя выполняем вход
        login(self.request, self.object)  # self.object - это новый зарегистрированный пользователь
        return response


class UserProfileCreateView(UpdateView):
    """
    Класс UserProfileCreateView наследуется от CreateView.
    Отвечает за 2й этап регистрации пользователя (добавление личных данных)
    """
    template_name = 'user_part/edit_data.html'
    success_url = reverse_lazy('register_address')

    def check_is_staff(self):
        return self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, завершил ли пользователь первый этап регистрации
        if not self.request.user.is_authenticated:
            return redirect('register')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Получаем профиль пользователя или создаем его, если не существует
        user = self.request.user
        model = DoctorProfile if user.is_staff else UserProfile
        obj, created = model.objects.get_or_create(user=user)
        obj.slug = user.username
        return obj

    def get_form_class(self):
        return CustomUpdateDoctorForm if self.check_is_staff() else CustomUpdateUserForm


class UserAddressCreateView(UpdateView):
    """
    Класс UserAddressCreateView наследуется от CreateView.
    Отвечает за 3й этап регистрации пользователя (добавление данных об адресе)
    """
    model = Address
    template_name = 'user_part/edit_address.html'
    form_class = CustomUpdateUserAddressForm

    def check_model(self):
        user = self.request.user
        return user.doctor_profile if user.is_staff else user.user_profile

    def form_valid(self, form):
        # Сначала сохраняем профиль пользователя в переменную user_address
        user_address = form.save(commit=False)
        user_profile = self.check_model()
        user_profile.address = user_address
        user_address.save()
        user_profile.save()
        # После успешного создания адреса, переходим по URL
        return super().form_valid(form)

    def get_object(self, queryset=None):
        user_profile = self.check_model()
        if user_profile.address:
            return user_profile.address
        return Address()

    def get_success_url(self):
        user_profile = self.check_model()
        return reverse_lazy('lk', kwargs={'slug': user_profile.slug})


class UserLk(DetailView):
    """
    Класс UserLk наследуется от DetailView.
    Через метод get_object мы получаем объект модели UserProfile или DoctorProfile
    и используем данные в get_context_data.
    """
    template_name = 'user_part/lk.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return get_object_or_404(DoctorProfile if user.is_staff else UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = self.get_object()
        context['user_data'] = user_data
        context['records'] = user_data.records
        context['records_count'] = user_data.records.count()
        context['age'] = calculate_age(user_data.birthday)
        context['address'] = user_data.address
        return context


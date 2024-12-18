from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, DoctorProfile


class UserViewsTestCase(TestCase):
    def setUp(self):
        """
        Создаем тестового пользователя, профиль и клиента для тестов
        """
        self.client = Client()

        # Создание обычного пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            is_staff=False
        )
        self.profile = UserProfile.objects.create(user=self.user,
                                                  name="Test User",
                                                  slug='test_user')

        # Создание доктора
        self.doctor_user = User.objects.create_user(
            username='doctoruser',
            password='password123',
            is_staff=True
        )
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user,
                                                           name="Doctor User",
                                                           slug='test_doctor')

        # URLы
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.register_profile_url = reverse('register_profile')
        self.lk_url = reverse('lk', kwargs={'slug': self.profile.slug})

    def test_home_view(self):
        """
        Проверка доступности домашней страницы
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_part/home.html')

    def test_user_login_view_authenticated_redirects_to_lk(self):
        """
        Проверка редиректа на ЛК после успешного логина
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        """
        Тест регистрации пользователя через UserCreateView
        """
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'test123@mail.ru',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_profile_create_view_get(self):
        """
        Тест получения формы для создания профиля пользователя
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.register_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_part/edit_data.html')

    def test_user_address_create_view(self):
        """
        Тест заполнения адреса пользователя
        """
        self.client.login(username='testuser', password='password123')
        address_url = reverse('edit_address', kwargs={'slug': self.profile.slug})
        response = self.client.post(address_url, {
            'country': 'Country',
            'city': 'Test City',
            'street': '123 Test Street',
            'house_number': 123,
            'flat_number': 123
        })
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Успешный редирект
        self.assertIsNotNone(self.profile.address)
        self.assertEqual(self.profile.address.city, 'Test City')

    def test_user_lk_view_for_user(self):
        """
        Тест отображения личного кабинета для обычного пользователя
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.lk_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_part/lk.html')
        self.assertContains(response, 'Test User')

    def test_user_lk_view_for_doctor(self):
        """
        Тест отображения личного кабинета для доктора
        """
        self.client.login(username='doctoruser', password='password123')
        doctor_lk_url = reverse('lk', kwargs={'slug': self.doctor_profile.slug})
        response = self.client.get(doctor_lk_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_part/lk.html')
        self.assertContains(response, 'Doctor User')


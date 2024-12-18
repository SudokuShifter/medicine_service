from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user_part.models import UserProfile, DoctorProfile
from .models import Question, Answer, Category


class FAQTestCase(TestCase):
    def setUp(self):
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

        self.category = Category.objects.create(name='Вопросы')

        self.question = Question.objects.create(name='Question', description='Question 1',
                                           patient=self.profile, category=self.category)


    def get_or_none(self, model, pk):
        try:
            return model.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None

    def test_question_view(self):
        for i in range(15):
            Question.objects.create(name=f'Question{i}', description='some description',
                                    patient=self.profile, category=self.category)

        url = reverse('faq_main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FAQ_main.html')
        self.assertEqual(len(response.context['questions']), 10)

    def test_add_question(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('add_question')
        response = self.client.post(url, {'name': 'Вопросffffff', 'description': 'Больffffff',
                                               'category': self.category, 'patient': self.profile.pk})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FAQ_form.html')

    def test_detail_question_view(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('detail_question', kwargs={'pk': self.question.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FAQ_view.html')

    def test_answer_question_view(self):
        self.client.login(username='doctoruser', password='password123')
        url = reverse('answer_question', kwargs={'pk': self.question.pk})
        response = self.client.post(url, {'answer': 'Привет', 'doctor': self.doctor_profile.pk})
        self.assertEqual(response.status_code, 302)
        answer = Answer.objects.get(pk=self.question.pk)
        self.assertEqual(answer.answer, 'Привет')

    def test_delete_question_view(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('delete_question', kwargs={'pk': self.question.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.get_or_none(Question, pk=self.question.pk))

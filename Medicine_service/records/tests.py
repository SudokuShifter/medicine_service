from django.db.models import Count
from django.test import TestCase, Client
from django.urls import reverse
from user_part.models import UserProfile, DoctorProfile, Position, Address, User
from .models import PatientDoctorRelation, PatientRecord


class DoctorListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            is_staff=False
        )
        self.profile = UserProfile.objects.create(user=self.user,
                                                  name="Test User",
                                                  slug='test_user')

        self.doctor_user = User.objects.create_user(
            username='doctoruser',
            password='password123',
            is_staff=True
        )
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user,
                                                           name="Doctor User",
                                                           slug='test_doctor')

    @staticmethod
    def fill_doctors():
        for i in range(15):
            DoctorProfile.objects.create(user=User.objects.create_user(username=f'testuser{i}',
                                                                       password=f'Password{i}+{i}',
                                                                       is_staff=True),
                                         name='Doctor User',
                                         slug=f'test_doctor{i}')


    def test_doctors_list_view(self):
        self.client.login(username='testuser', password='password123')
        DoctorListViewTest.fill_doctors()
        response = self.client.get(reverse('doc_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctors.html')
        self.assertEqual(len(response.context['doctors']), 10)

    def test_rate_doctor_view(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('rate_doc', kwargs={'pk': self.doctor_profile.pk})
        response = self.client.post(url, data={'action': 'like'})
        self.assertEqual(response.status_code, 302)
        rating = PatientDoctorRelation.objects.filter(doctor_id=self.doctor_profile.pk, like=True).count()
        self.assertEqual(rating, 1)

    def test_create_record(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('record_doc', kwargs={'pk': self.doctor_profile.pk})
        response = self.client.post(url, data={'appointment_date': '2025-12-15 15:55:00'})
        self.assertRedirects(response, '/records/my_records/', status_code=302, target_status_code=200)
        record = PatientRecord.objects.get(pk=self.doctor_profile.pk)
        self.assertEqual(str(record.appointment_date), '2025-12-15 15:55:00+00:00')

    def test_check_records(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('check_records')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'check_records.html')
        self.assertEqual(len(response.context['records']), 0)

    def test_update_record(self):
        self.client.login(username='testuser', password='password123')
        """Дописать"""
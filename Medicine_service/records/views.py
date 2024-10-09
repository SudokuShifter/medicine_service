from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, View
from django.views.generic.edit import BaseCreateView
from django.db.models import Count, Q
from django.urls import reverse_lazy

from .models import PatientDoctorRelation, PatientRecord
from user_part.models import DoctorProfile, Position
from .forms import RecordForm


class DoctorListView(ListView):
    """
    Класс DoctorListView наследуется от ListView. Определён с целью отображения списка доступных докторов,
    которые могут принять пациента по записи.
    Свойство paginate_by - параметр отображения объектов на 1 странице, то есть ограничитель в 10 экземпляров.
    Так же переопределён метод get_queryset, чтобы соответствовать реализуемой фильтрации внутри шаблона.
    """
    model = DoctorProfile
    template_name = 'doctors.html'
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        position = self.request.GET.get('position')
        city = self.request.GET.get('city')
        search = self.request.GET.get('search')
        if position and position != 'Все':
            queryset = queryset.filter(position__title=position)
        if city and city != 'Все':
            queryset = queryset.filter(address__city=city)
        if search:
            queryset = queryset.filter(second_name__icontains=search)
        queryset = queryset.annotate(
            likes=Count('rating', filter=Q(rating__like=True)),
            dislikes=Count('rating', filter=Q(rating__dislike=True))
        )
        queryset = queryset.order_by('created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position'] = Position.objects.values_list('title', flat=True)
        context['city'] = (DoctorProfile.objects.filter(address__isnull=False)
                           .values_list('address__city', flat=True).distinct())
        return context


class RateDoctorView(View):
    """
    Класс RateDoctorView наследуется от базового класса View. В классе определён метод post,
    для передачи оценки (лайк/дизлайк) в модель PatientDoctorRelation со связью Многие Ко Многим.
    Через шаблон передаётся action, pk врача и pk пациента и вносится в базу данных.
    При этом комбинация врача и пациента должна быть уникальной, чтобы пациент не смог поставить более 1й оценки врачу
    """
    def post(self, request, pk):
        doctor = DoctorProfile.objects.get(pk=pk)
        patient = self.request.user.user_profile
        action = request.POST.get('action')
        relation, created = (PatientDoctorRelation.objects.
                             get_or_create(patient=patient, doctor=doctor))
        relation.like, relation.dislike = (True, False) if action == 'like' else (False, True)
        relation.save()
        return redirect('doc_list')


class CreateRecord(CreateView):
    model = PatientRecord
    form_class = RecordForm
    template_name = 'record_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = self.request.user.user_profile
        context['doctor_data'] = DoctorProfile.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        user_profile = self.request.user.user_profile
        return reverse_lazy('lk', kwargs={'slug': user_profile.slug})

    def form_valid(self, form):
        patient_record = form.save(commit=False)
        patient_record.doctor = DoctorProfile.objects.get(pk=self.kwargs.get('pk'))
        patient_record.patient = self.request.user.user_profile
        return super().form_valid(form)

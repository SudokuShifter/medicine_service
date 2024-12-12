from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, View
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Count, Q, ExpressionWrapper, F, IntegerField
from django.urls import reverse_lazy

from .models import PatientDoctorRelation, PatientRecord
from user_part.models import DoctorProfile, Position
from .forms import RecordForm, SetStatusRecordForm


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
    """
    Класс CreateRecord наследуется от CreateView. В классе реализован достаточно стандартный интерфейс
    для сбора данных из формы с занесением в бд. Класс работает с моделью записи пациента - PatientRecord
    и формой для создания записей - RecordForm
    """
    model = PatientRecord
    form_class = RecordForm
    template_name = 'record_form.html'
    success_url = reverse_lazy('check_records')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = self.request.user.user_profile
        context['doctor_data'] = DoctorProfile.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        patient_record = form.save(commit=False)
        patient_record.doctor = DoctorProfile.objects.get(pk=self.kwargs.get('pk'))
        patient_record.patient = self.request.user.user_profile
        return super().form_valid(form)


class CheckRecords(ListView):
    """
    Класс CheckRecords наследуется от ListView. Служит для отображения списка записей.
    Переопределён метод get_queryset для прокидывания записей пользователя в темплейт.
    В темплейте queryset называется records
    """
    model = PatientRecord
    template_name = 'check_records.html'
    context_object_name = 'records'


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = PatientRecord.objects.filter(patient=self.request.user.user_profile)
        queryset.order_by('appointment_date')
        return queryset


class UpdateRecord(UpdateView):
    """
    Класс UpdateRecord наследуется от UpdateView. Служит для обновления информации внутри определённой записи.
    Можно было бы совместить логику с Классом CreateRecord, но я посчитал, что так будет лаконичнее и правильнее
    с точки зрения гибкости последующей настройки
    """
    model = PatientRecord
    template_name = 'record_update_form_patient.html'
    form_class = RecordForm
    context_object_name = 'record'
    success_url = reverse_lazy('check_records')


class DeleteRecord(DeleteView):
    """
    Класс DeleteRecord наследуется от DeleteView. Служит для удаления определённой записи.
    """
    model = PatientRecord
    template_name = 'delete_popup.html'
    context_object_name = 'record'
    success_url = reverse_lazy('check_records')


class DoctorRateView(ListView):
    """
    Класс DoctorRateView наследуется от ListView. Служит для просмотра рейтинга врачей.
    Переопределён метод get_queryset для отображения докторов в правильном порядке (от б-го кол-ва лайков до меньшего)
    """
    model = DoctorProfile
    template_name = 'doctor_rate.html'
    context_object_name = 'doctor_profiles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            like_count = Count('rating', filter=Q(rating__like=True)),
            dislike_count = Count('rating', filter=Q(rating__dislike=True)),
            rating_score = ExpressionWrapper(
                F('like_count') - F('dislike_count'),
                output_field=IntegerField()
            )).order_by('-rating_score')
        return queryset


class DoctorRecordsView(ListView):
    """
    Класс DoctorRecordsView наследуется от ListView. Служит для просмотра записей пациентов.
    Переопределён метод get_queryset для отображения записей в правильном порядке.
    """
    model = PatientRecord
    template_name = 'doctor_check_records.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = PatientRecord.objects.filter(doctor=self.request.user.doctor_profile
                                                ).order_by('-appointment_date')
        return queryset



class UpdateRecordStatus(UpdateView):
    """
    UpdateRecordStatus наследуется от UpdateView. Служит для обновления информации в записи пациента.
    """
    model = PatientRecord
    template_name = 'record_update_form.html'
    form_class = SetStatusRecordForm
    context_object_name = 'record'
    success_url = reverse_lazy('patient_records')

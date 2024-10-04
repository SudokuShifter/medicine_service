from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, View
from django.db.models import Count, Q

from .models import PatientDoctorRelation
from user_part.models import DoctorProfile, Position


class DoctorListView(ListView):
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
    def post(self, request, pk):
        doctor = DoctorProfile.objects.get(pk=pk)
        patient = self.request.user.user_profile
        action = request.POST.get('action')
        relation, created = (PatientDoctorRelation.objects.
                             get_or_create(patient=patient, doctor=doctor))
        relation.like, relation.dislike = (True, False) if action=='like' else (False, True)
        relation.save()
        return redirect('doc_list')
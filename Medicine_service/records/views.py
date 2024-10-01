from django.shortcuts import render
from django.views.generic import CreateView, ListView
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
        queryset = queryset.order_by('created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position'] = Position.objects.values_list('title', flat=True)
        context['city'] = (DoctorProfile.objects.filter(address__isnull=False)
                           .values_list('address__city', flat=True).distinct())
        return context

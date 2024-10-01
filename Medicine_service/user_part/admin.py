from django.contrib import admin
from .models import Position, DoctorProfile
# Register your models here.


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    fields = ['title', 'description']

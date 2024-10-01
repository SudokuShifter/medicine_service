from django.contrib import admin
from .models import Position, DoctorProfile
# Register your models here.


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    fields = ['title', 'description']


@admin.register(DoctorProfile)
class DoctorAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'second_name', 'middle_name', 'birthday', 'slug', 'photo', 'position', 'address']
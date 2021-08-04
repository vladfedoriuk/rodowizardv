from django.contrib import admin
from .models import Training, PersonalData
from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, time
from .forms import TrainingForm


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "email", "start_time", "end_time")
    list_filter = ("start_time", "end_time")
    search_fields = ("title", "email")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_time"
    ordering = ("-start_time", "end_time")
    form = TrainingForm


@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "email", "phone_number", "training")
    search_fields = ("name", "surname", "email")
    ordering = ("surname", "name")
    list_filter = ("training",)

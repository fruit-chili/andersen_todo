from django.contrib import admin

from .models import Task


@admin.register(Task)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'title', 'description', 'status']
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.reverse import reverse

from tasks.models import Task
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import models


class TaskSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id', 'user_id', 'username', 'title', 'description', 'status']
    def get_username(self, obj):
        return obj.user_id.username

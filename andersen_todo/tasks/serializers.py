from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id', 'user_id', 'username', 'title', 'description', 'status']
    def get_username(self, obj):
        return obj.user_id.username

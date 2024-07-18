from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    class TaskStatus(models.TextChoices):
        NEW = 'New'
        IN_PROGRESS = 'In Progress'
        COMPLETED = 'Completed'
    user_id = models.ForeignKey(User,
                            on_delete=models.CASCADE, 
                            related_name='tasks')
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True, 
                             max_length=1024)
    status = models.CharField(choices=TaskStatus.choices, 
                                default=TaskStatus.NEW)
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return f'[Task id{self.id}: "{self.title[0:15]}..." (User {self.user_id.username})]'          
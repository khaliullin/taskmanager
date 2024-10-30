from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class DefaultFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(DefaultFields):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    assigned_to = models.ForeignKey(
        User,
        related_name='tasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_overdue(self):
        """Task is not completed and deadline is expired."""
        if self.deadline and not self.completed_at:
            return timezone.now() > self.deadline
        return False


class Comment(DefaultFields):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class TaskFile(DefaultFields):
    task = models.ForeignKey(Task, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_files/')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

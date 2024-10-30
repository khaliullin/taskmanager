from django.contrib import admin
from django.utils import timezone

from tasks.models import Task, TaskFile, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'deadline', 'completed_at')
    search_fields = ('title',)
    autocomplete_fields = ('assigned_to',)
    actions = ('mark_completed',)

    @admin.action(description='Mark selected tasks as completed')
    def mark_completed(self, request, queryset):
        queryset.update(completed_at=timezone.now())


@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'file')
    autocomplete_fields = ('task', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author')
    autocomplete_fields = ('task', 'author')

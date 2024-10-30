from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task, Comment, TaskFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'assigned_to',
            'completed_at',
            'deadline',
            'created_at',
            'updated_at',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'author',
            'created_at',
        )
        read_only_fields = ('author', 'created_at')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['task'] = Task.objects.get(
            pk=self.context['view'].kwargs['task_pk']
        )
        return super().create(validated_data)


class TaskDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'deadline', 'completed_at', 'comments')


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('id', 'file', 'user', 'task', 'created_at')
        read_only_fields = ('user', 'task', 'created_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['task'] = Task.objects.get(
            pk=self.context['view'].kwargs['task_pk']
        )
        return super().create(validated_data)

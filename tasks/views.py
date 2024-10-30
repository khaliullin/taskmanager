from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from tasks.filters import TaskFilter
from tasks.models import Task, Comment, TaskFile
from tasks.serializers import (
    TaskSerializer,
    CommentSerializer,
    TaskFileSerializer,
    TaskDetailSerializer,
    UserSignUpSerializer,
)

User = get_user_model()


class UserSignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        if self.action == 'retrieve':
            return Task.objects.prefetch_related('comments__author')
        return Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'status': 'user not found'}, status=status.HTTP_404_NOT_FOUND
            )

        task.assigned_to = user
        task.save()
        return Response({'status': 'assigned'})

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.completed_at = timezone.now()
        task.save()
        return Response({'status': 'task marked as completed'})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_pk']).select_related(
            'author'
        )

    def get_serializer_context(self):
        return {'request': self.request, 'view': self}


class TaskFileViewSet(viewsets.ModelViewSet):
    serializer_class = TaskFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskFile.objects.filter(task_id=self.kwargs['task_pk'])

    def get_serializer_context(self):
        return {'request': self.request, 'view': self}

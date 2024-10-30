import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from tasks.models import Task

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def task(db, user):
    return Task.objects.create(
        title='Test Task',
        description='This is a test task.',
        deadline=None,
        completed_at=None,
    )


@pytest.fixture
def overdue_task(db, user):
    return Task.objects.create(
        title='Overdue Task',
        description='This task is overdue.',
        deadline=timezone.now() - timezone.timedelta(days=1),
        completed_at=None,
    )


@pytest.fixture
def completed_task(db, user):
    task = Task.objects.create(
        title='Completed Task',
        assigned_to=user,
        description='This task was completed before deadline.',
        deadline=timezone.now() + timezone.timedelta(days=2),
        completed_at=timezone.now() - timezone.timedelta(days=1),
    )
    return task

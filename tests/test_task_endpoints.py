from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from tasks.models import Comment
from tests.fixtures import api_client, user, task, overdue_task, completed_task


def test_create_task(api_client):
    url = reverse('task-list')
    data = {
        'title': 'New Task',
        'description': 'Task description',
        'deadline': (timezone.now() + timezone.timedelta(days=2)).isoformat(),
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'New Task'


def test_task_detail_view_with_comments(api_client, task, user):
    comment = Comment.objects.create(task=task, author=user, content='Test comment')
    url = reverse('task-detail', args=[task.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == task.title
    assert 'comments' in response.data
    assert response.data['comments'][0]['content'] == comment.content


def test_filter_overdue_tasks(api_client, task, overdue_task, completed_task):
    url = reverse('task-list')
    response = api_client.get(url, {'is_overdue': 'true'})
    assert response.status_code == status.HTTP_200_OK
    task_ids = {task['id'] for task in response.data}
    assert overdue_task.id in task_ids
    assert completed_task.id not in task_ids
    assert task.id not in task_ids


def test_filter_completed_tasks(api_client, task, overdue_task, completed_task):
    url = reverse('task-list')
    response = api_client.get(url, {'is_completed': 'true'})
    assert response.status_code == status.HTTP_200_OK
    task_ids = {task['id'] for task in response.data}
    assert completed_task.id in task_ids
    assert task.id not in task_ids
    assert overdue_task.id not in task_ids


def test_filter_tasks_with_deadline(api_client, task, overdue_task, completed_task):
    url = reverse('task-list')
    response = api_client.get(url, {'has_deadline': 'true'})
    assert response.status_code == status.HTTP_200_OK
    task_ids = {task['id'] for task in response.data}
    assert completed_task.id in task_ids
    assert overdue_task.id in task_ids
    assert task.id not in task_ids


def test_filter_assigned_task(api_client, user, task, overdue_task, completed_task):
    url = reverse('task-list')
    response = api_client.get(url, {'assigned_to': user.id})
    assert response.status_code == status.HTTP_200_OK
    task_ids = {task['id'] for task in response.data}
    assert completed_task.id in task_ids
    assert task.id not in task_ids
    assert overdue_task.id not in task_ids


def test_create_comment_on_task(api_client, task):
    url = reverse('task-comments-list', args=[task.id])
    data = {
        'content': 'This is a test comment.',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['content'] == 'This is a test comment.'
    assert response.data['author']['id'] == api_client.handler._force_user.id


def test_file_upload_for_task(api_client, task):
    url = reverse('task-files-list', args=[task.id])
    with open('test_file.txt', 'w') as f:
        f.write('This is a test file.')
    with open('test_file.txt', 'rb') as f:
        response = api_client.post(url, {'file': f}, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['task'] == task.id
    assert response.data['user'] == api_client.handler._force_user.id

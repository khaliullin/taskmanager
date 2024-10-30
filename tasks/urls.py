from django.urls import path, include
from rest_framework_nested import routers
from .views import TaskViewSet, TaskFileViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)

tasks_router = routers.NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'files', TaskFileViewSet, basename='task-files')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tasks_router.urls)),
]

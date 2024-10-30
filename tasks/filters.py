from django_filters import rest_framework as filters
from django.utils import timezone
from tasks.models import Task


class TaskFilter(filters.FilterSet):
    has_deadline = filters.BooleanFilter(
        field_name='deadline',
        lookup_expr='isnull',
        exclude=True,
    )
    is_completed = filters.BooleanFilter(
        field_name='completed_at',
        lookup_expr='isnull',
        exclude=True,
    )
    is_overdue = filters.BooleanFilter(method='filter_is_overdue')
    assigned_to = filters.NumberFilter(field_name='assigned_to__id')

    class Meta:
        model = Task
        fields = ('has_deadline', 'is_completed', 'is_overdue', 'assigned_to')

    def filter_is_overdue(self, qs, name, value):
        qs = qs.filter(
            completed_at__isnull=True,
            deadline__isnull=False,
        )
        if value:
            return qs.filter(deadline__lt=timezone.now())

        return qs.filter(deadline__gte=timezone.now())

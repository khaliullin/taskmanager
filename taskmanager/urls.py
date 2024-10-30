from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from tasks.views import UserSignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/tasks/', include('tasks.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title='Task Manager API',
        default_version='v1',
        description='API documentation for the Task Manager application',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

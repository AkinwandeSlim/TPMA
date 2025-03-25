# Main urls

from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from lesson_plan.views import LessonPlanViewSet
from reports.views import ReportViewSet




schema_view = get_schema_view(
   openapi.Info(
      title="TPMA API",
      default_version='v1',
      description="",
      terms_of_service="https://www.emis.test/policies/terms/",
      contact=openapi.Contact(email="contact@emis.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# Define the router
router = DefaultRouter()
router.register(r'lesson-plans', LessonPlanViewSet, basename='lesson-plans')
router.register(r'reports', ReportViewSet, basename='reports')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls', namespace='authentication')),
    path('api/', include('social_django.urls', namespace='social')),
    path('api/administrator/', include('administrator.urls', namespace='administrator')),
    path('api/staff/', include('staff.urls', namespace='staff')),
    path('api/file/', include('file_handler.urls', namespace='file_handler')),
    path('api/email/', include('email_handler.urls', namespace='email_handler')),
    path('api/', include('miscellaneous.urls', namespace='miscellaneous')),
    path('api/core/', include('core.urls', namespace='core')),
    path('api/academy/', include('academy.urls', namespace='academy')),
    path('api/', include('comments.urls', namespace='comments')),
    path('api/calendar/', include('academic_calendar.urls', namespace='academic_calendar')),
    path('api/press/', include('press.urls', namespace='press')),
    path('api/', include(router.urls)),  # Router for lesson-plans and reports
    path('doc/swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


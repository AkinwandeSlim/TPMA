# supervisor/urls.py

app_name = 'supervisor'

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SupervisorViewSet, SupervisorUsersView, SupervisorPartialUpdate, SupervisorDeleteView, GetSupervisorView

router = DefaultRouter()
router.register(r'', SupervisorViewSet, basename='Supervisor')

urlpatterns = [
    path('users/', SupervisorUsersView.as_view(), name='supervisor_users_view'),
    path('profile/', GetSupervisorView.as_view(), name='get_supervisor_view'),
    path('update-partial/<int:pk>/', SupervisorPartialUpdate.as_view(), name='supervisor-partial-update'),
    path('delete/<int:pk>/', SupervisorDeleteView.as_view(), name='supervisor-delete'),
    path('', include(router.urls)),
]



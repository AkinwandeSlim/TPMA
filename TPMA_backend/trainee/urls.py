# trainee/urls.py

app_name = 'trainee'

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    TraineeViewSet, 
    TraineeUsersView, 
    TraineePartialUpdate, 
    TraineeDeleteView, 
    GetTraineeView,
    TraineeRetrieveView,
)

router = DefaultRouter()
router.register(r'', TraineeViewSet, basename='trainee')


urlpatterns = [
    path('users/', TraineeUsersView.as_view(), name='trainee_users_view'),
    path('profile/', GetTraineeView.as_view(), name='get_trainee_view'),
    path('update-partial/<int:pk>/', TraineePartialUpdate.as_view(), name='trainee_partial_update'),
    path('delete/<int:pk>/', TraineeDeleteView.as_view(), name='trainee_delete'),
    path('id/<str:user__username>/', TraineeRetrieveView.as_view(), name='trainee-detail'),
    path('', include(router.urls)),
]



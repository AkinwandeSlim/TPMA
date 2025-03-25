# trainee/views.py

import json
from academy.views import TraineeEnrollmentAPIView
from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.views import UserDeleteView
from datetime import date
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from rest_framework import status, generics, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trainee
from .serializers import TraineeSerializer, TraineeUsersSerializer



class TraineeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer

    def create(self, request, *args, **kwargs):
        trainee_data = request.data.copy()
        user_data = json.loads(trainee_data.pop('user')[0])
        user_data["role"] = "trainee"
        user_data["is_staff"] = False
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        trainee_data['user'] = user.id

        try:
            serializer = self.get_serializer(data=trainee_data)
            serializer.is_valid(raise_exception=True)
            trainee = serializer.save()
        except Exception as e:
            # Delete the newly created user if creating the teacher fails
            user.delete()

            error_messages = {}
            for field, errors in e.detail.items():
                error_messages[field] = str(errors[0])

            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class TraineeUsersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        trainee_users = User.objects.filter(role='trainee')
        serialized_users = serializers.serialize('json', trainee_users, fields=('username', 'first_name', 'last_name', 'email', 'is_active'))
        return HttpResponse(serialized_users, content_type='application/json')



class CustomJSONEncoder(serializers.json.DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)



class GetTraineeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.GET.get('reference')
        try:
            trainee = Trainee.objects.get(user_id=user_id)
            user = User.objects.select_related('trainee').values(
                'last_login', 'username', 'first_name', 'last_name',
                'email', 'is_staff', 'is_active', 'date_joined', 'role', 'middle_name', 'id'
            ).get(trainee=trainee)
            user_added_by = trainee.added_by.username
            user_updated_by = ''
            if trainee.updated_by:
                user_updated_by = trainee.updated_by.username

            trainee_data = serializers.serialize('python', [trainee])
            user_data = {
                'username': user['username'],
                'first_name': user['first_name'],
                'middle_name': user['middle_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'role': user['role'],
                'is_staff': user['is_staff'],
                'is_active': user['is_active'],
                'date_joined': user['date_joined'],
                'last_login': user['last_login'],
                'id': user['id'],
            }

            combined_data = trainee_data[0]
            combined_data['fields']['added_by'] = user_added_by
            combined_data['fields']['updated_by'] = user_updated_by
            combined_data['fields']['user'] = user_data
            
            try:
                trainee_id = int(trainee.id)
                combined_data['fields']['enrollment'] = TraineeEnrollmentAPIView().enrollment(trainee_id)
            except Exception as e:
                combined_data['fields']['enrollment'] = None

            serialized_data = json.dumps(combined_data, cls=CustomJSONEncoder)
            return HttpResponse(serialized_data, content_type='application/json')
        except Trainee.DoesNotExist:
            return JsonResponse({'error': 'Trainee not found'}, status=404)



class TraineePartialUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class TraineeDeleteView(DestroyModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Trainee.objects.all()
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user:
            user_id = instance.user.id
            user_delete_view = UserDeleteView()
            response = user_delete_view.delete(request, user_id)
            if response.status_code != 204:
                return response
        return self.destroy(request, *args, **kwargs)



class TraineeRetrieveView(generics.RetrieveAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeUsersSerializer
    lookup_field = 'user__username'  # Look up trainee by user's username
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Add enrollment data to the response
        combined_data = serializer.data
        try:
            trainee_id = int(instance.id)
            combined_data['enrollment'] = TraineeEnrollmentAPIView().enrollment(trainee_id)
        except Exception as e:
            combined_data['enrollment'] = None
        
        return Response(combined_data)




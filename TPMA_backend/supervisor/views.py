# Supervisor/views.py

import json
from datetime import date
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from rest_framework import status, generics, viewsets
from rest_framework.mixins import DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from academy.views import SupervisorEnrollmentAPIView
from authentication.models import User
from authentication.serializers import UserSerializer
from .models import Supervisor
from .serializers import SupervisorSerializer, SupervisorViewSetSerializer
from authentication.views import UserDeleteView
from rest_framework.views import APIView



class SupervisorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorViewSetSerializer

    def create(self, request, *args, **kwargs):
        supervisor_data = request.data.copy()
        user_data = json.loads(supervisor_data.pop('user')[0])
        user_data["role"] = "supervisor"
        user_data["is_staff"] = True
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        

        supervisor_data['user'] = user.id

        try:
            serializer = self.get_serializer(data=supervisor_data)
            serializer.is_valid(raise_exception=True)
            supervisor = serializer.save()
        except Exception as e:
            # Delete the newly created user if creating the supervisor fails
            user.delete()

            error_messages = {}
            for field, errors in e.detail.items():
                error_messages[field] = str(errors[0])

            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)


        return Response(serializer.data, status=status.HTTP_201_CREATED)



class SupervisorUsersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        supervisor_users = User.objects.filter(role='supervisor')
        serialized_users = serializers.serialize('json', supervisor_users, fields=('username', 'first_name', 'last_name', 'email', 'is_active'))
        return HttpResponse(serialized_users, content_type='application/json')



class CustomJSONEncoder(serializers.json.DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)



class GetSupervisorView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.GET.get('reference')
        try:
            supervisor = Supervisor.objects.get(user_id=user_id)
            user = User.objects.select_related('supervisor').values(
                'last_login', 'username', 'first_name', 'last_name',
                'email', 'is_staff', 'is_active', 'date_joined', 'role', 'middle_name', 'id'
            ).get(supervisor=supervisor)
            user_added_by = supervisor.added_by.username
            user_updated_by = ''
            if supervisor.updated_by:
                user_updated_by = supervisor.updated_by.username

            supervisor_data = serializers.serialize('python', [supervisor])
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

            combined_data = supervisor_data[0]
            combined_data['fields']['added_by'] = user_added_by
            combined_data['fields']['updated_by'] = user_updated_by
            combined_data['fields']['user'] = user_data
            
            try:
                supervisor_id = int(supervisor.id)
                combined_data['fields']['enrollment'] = SupervisorEnrollmentAPIView().enrollment(supervisor_id)
            except Exception as e:
                combined_data['fields']['enrollment'] = None
            
            serialized_data = json.dumps(combined_data, cls=CustomJSONEncoder)
            return HttpResponse(serialized_data, content_type='application/json')
        except Supervisor.DoesNotExist:
            return JsonResponse({'error': 'Supervisor not found'}, status=404)



class SupervisorPartialUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class SupervisorDeleteView(DestroyModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Supervisor.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user:
            user_id = instance.user.id
            user_delete_view = UserDeleteView()
            response = user_delete_view.delete(request, user_id)
            if response.status_code != 204:
                return response
        return self.destroy(request, *args, **kwargs)


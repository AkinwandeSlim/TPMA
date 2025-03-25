from rest_framework import serializers
# from .models import Teacher
from authentication.serializers import UserSerializer, UserBriefSerializer
from .models import Supervisor

class SupervisorViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = "__all__" 


class supervisorSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the UserSerializer to serialize the user related fields
    class Meta:
        model = Supervisor
        fields = "__all__" 


class SupervisorBriefSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer()  # Use the UserBriefSerializer to serialize the user related fields 
    class Meta:
        model = Supervisor
        fields = ['id', 'acronym', 'phone', 'photo_id', 'gender', 'user']




class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = '__all__'

# student/serializers.py 

from rest_framework import serializers
from .models import Trainee
from authentication.serializers import UserSerializer2, UserBriefSerializer, UserSerializer



class TraineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = "__all__" 



class TraineeNestedSerializer(serializers.ModelSerializer):
    user = UserSerializer2(read_only=True)
    class Meta:
        model = Trainee
        fields = "__all__" 



class TraineeUsersSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer()
    class Meta:
        model = Trainee
        fields = "__all__" 




# class TraineeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trainee
#         fields = '__all__'

from rest_framework import serializers
from .models import LessonPlan

class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = ['id', 'title', 'content', 'trainee', 'supervisor', 'file', 'created_at', 'updated_at']
from rest_framework import viewsets
from .models import LessonPlan
from .serializers import LessonPlanSerializer

class LessonPlanViewSet(viewsets.ModelViewSet):
    queryset = LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer
    
    
    
    
    




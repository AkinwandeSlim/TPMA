from django.db import models
from trainee.models import Trainee  # Import from trainee app
from supervisor.models import Supervisor  # Import from supervisor app

class LessonPlan(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='lesson_plans')
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_plans')
    file = models.FileField(upload_to='lesson_plans/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.trainee.last_name}"
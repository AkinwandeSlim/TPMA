from django.db import models
from trainee.models import Trainee
from supervisor.models import Supervisor
from lesson_plan.models import LessonPlan  # Import from lesson_plan app

class Report(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='reports')
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_reports')
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    feedback = models.TextField()
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.trainee.last_name} - {self.created_at}"
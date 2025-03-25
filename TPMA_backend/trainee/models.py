from django.db import models
from django.conf import settings

class Trainee(models.Model):
    GENDER_CHOICES = (('U', 'Undefined'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other'))
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    progress = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(default='U', choices=GENDER_CHOICES, max_length=1)
    permanent_address = models.TextField(blank=True, null=True)
    present_address = models.TextField(blank=True, null=True)
    nid = models.CharField(default=None, max_length=20, unique=True)
    photo_id = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trainee_updated_by', on_delete=models.SET_NULL, blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trainee_added_by', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    history = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
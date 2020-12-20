from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    university = models.CharField(max_length=100, null=False, blank=True, default='')
    field = models.CharField(max_length=100, null=False, blank=True, default='')
    entrance_year = models.IntegerField()


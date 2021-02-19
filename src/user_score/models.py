from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from BookAdvertisement.models import BookAd


class AdScore(models.Model):
    advertisement = models.ForeignKey(BookAd, on_delete=models.CASCADE, primary_key=True, related_name="advertisement")
    score_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="score_owner")
    score = models.IntegerField(null=False, default=1)

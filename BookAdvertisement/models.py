from django.db import models


class BookAd(models.Model):
    id = models.IntegerField(primary_key=True)
    # poster = models.ImageField(upload_to='ad_posters/', null=True, blank=True, validators=None)
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    ad_type = models.BinaryField()

    def __str__(self):
        return self.title



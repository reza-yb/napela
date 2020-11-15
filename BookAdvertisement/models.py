from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class BookAd(models.Model):
    poster = models.ImageField(upload_to='ad_posters/', null=True, blank=True)
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    sell = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad', kwargs={'pk': self.pk})

    def clean(self):
        if self.poster and not self.sell:
            raise ValidationError("posters are not allowed for buy advertisements")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BookAd, self).save(*args, **kwargs)

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _


class BookAd(models.Model):
    class AdStatus(models.TextChoices):
        PENDING = "PENDING",
        ACCEPTED = "ACCEPTED",
        REJECTED = "REJECTED",
        DONE = "DONE"

        @classmethod
        def choices(cls):
            print(tuple((i.name, i.value) for i in cls))
            return tuple((i.name, i.value) for i in cls)

    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    poster = models.ImageField("تصویر", upload_to='ad_posters/', null=True, blank=True)
    title = models.CharField("نام کتاب", max_length=30, blank=False)
    author = models.CharField("نام نویسنده", max_length=30)
    description = models.TextField("توضیحات", max_length=500)
    sell = models.BooleanField("فروشی")
    suggested_money = models.IntegerField(verbose_name=_('suggested money'), default=0, null=False)
    status = models.CharField(max_length=255, choices=AdStatus.choices, verbose_name='status', default=AdStatus.PENDING)
    created_datetime = models.DateTimeField(null=False, auto_now_add=True, )
    modified_datetime = models.DateTimeField(null=False, default=timezone.datetime(year=2020, month=1, day=1))
    # scoring fields
    addresser = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="addresser")

    def __str__(self):
        return self.title

    def owner_score(self):
        all_ads = BookAd.objects.filter(owner=self.owner)
        scores = []
        for ad in all_ads:
            try:
                score = ad.advertisement.score
                scores.append(score)
            except:
                pass
        if len(scores) == 0:
            return "5.0"
        return "%.1f" % (sum(scores) / len(scores))

    def get_absolute_url(self):
        return reverse('BookAdvertisement:ad', kwargs={'pk': self.pk})

    def clean(self):
        if self.poster and not self.sell:
            raise ValidationError("posters are not allowed for buy advertisements")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BookAd, self).save(*args, **kwargs)

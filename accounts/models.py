from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), null=False, blank=False, on_delete=models.CASCADE)
    university = models.CharField(verbose_name=_('university'), max_length=100, null=False, blank=True, default='')
    field = models.CharField(verbose_name=_('field'), max_length=100, null=False, blank=True, default='')
    entrance_year = models.IntegerField(verbose_name=_('entrance_year'))


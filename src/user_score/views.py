from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.urls import reverse
from django_registration.backends.one_step.views import User

from BookAdvertisement.models import BookAd
from user_score.models import AdScore

links = [{"href": "/", "class": "item", "title": "صفحه اصلی"},
         {"href": "/ads", "class": "item", "title": "آگهی‌ها"},
         {"href": "/ads/new", "class": "item", "title": "ثبت آگهی"}]


@login_required
@user_passes_test(lambda u: u.is_superuser)
def set_advertisement_addresser_and_done(request, ad_id):
    ad: BookAd = get_object_or_404(BookAd, pk=ad_id)
    addresser_username = request.POST.get('addresser_username')
    addresser = get_object_or_404(User, username=addresser_username)
    if addresser != request.user:
        ad.status = BookAd.AdStatus.DONE
        ad.addresser = addresser
        ad.save()
        return HttpResponseRedirect(reverse('BookAdvertisement:ad', args=[ad_id]))
    else:
        raise PermissionDenied()


@login_required
def give_score(request, ad_id):
    ad: BookAd = get_object_or_404(BookAd, pk=ad_id)
    score = int(request.POST.get("score", 1))
    if ad.addresser == request.user and 1 <= score <= 5:
        if AdScore.objects.filter(pk=ad).count() == 0:
            ad_score = AdScore()
        else:
            ad_score = get_object_or_404(AdScore, pk=ad)
        ad_score.score_owner = ad.addresser
        ad_score.score = request.POST.get("score", 1)
        ad_score.advertisement = ad
        ad_score.save()
        return HttpResponseRedirect(reverse('BookAdvertisement:ad', args=[ad_id]))
    else:
        raise PermissionDenied()

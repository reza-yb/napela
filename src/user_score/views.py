from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.urls import reverse
from django_registration.backends.one_step.views import User

from BookAdvertisement.models import BookAd

links = [{"href": "/", "class": "item", "title": "صفحه اصلی"},
         {"href": "/ads", "class": "item", "title": "آگهی‌ها"},
         {"href": "/ads/new", "class": "item", "title": "ثبت آگهی"}]


@login_required
@user_passes_test(lambda u: u.is_superuser)
def set_advertisement_addresser_and_done(request, ad_id):
    ad: BookAd = get_object_or_404(BookAd, pk=ad_id)
    addresser_username = request.POST.get('addresser_username')
    addresser = get_object_or_404(User, username=addresser_username)
    ad.status = BookAd.AdStatus.DONE
    ad.addresser = addresser
    ad.save()
    return HttpResponseRedirect(reverse('BookAdvertisement:ad', args=[ad_id]))

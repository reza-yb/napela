from django.http import HttpResponse
from django.shortcuts import render
from .models import BookAd


def homePageView(request):
    return HttpResponse('Hello, World 2!')


def get_all_ads(request):
    template_name = 'all_ads.html'
    queryset = BookAd.objects.all()
    context = {"book_ads": queryset}
    return render(request, template_name, context)


def get_ad_info(request, ad_id):
    template_name = 'ad_info.html'
    ad = BookAd.objects.get(id=ad_id)
    context = {"ad": ad}
    return render(request, template_name, context)

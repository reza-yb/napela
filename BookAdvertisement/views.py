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

# def show_ad_info(request):
#     template_name =

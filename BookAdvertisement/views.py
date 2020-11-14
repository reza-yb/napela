from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from copy import deepcopy

from .models import BookAd

links = [{"href": "/", "class": "item", "title": "صفحه اصلی"},
         {"href": "/ads", "class": "item", "title": "آگهی ها"},
         {"href": "/ads/new", "class": "item", "title": "ثبت آگهی"}]


def homePageView(request):
    template_name = 'index.html'
    temp_links = deepcopy(links)
    temp_links[0]["class"] = "active item"
    context = {"page_title": "Home Page", "links": temp_links}
    return render(request, template_name, context)


def get_all_ads(request):
    template_name = 'all_ads.html'
    queryset = BookAd.objects.all()
    temp_links = deepcopy(links)
    temp_links[1]["class"] = "active item"
    context = {"page_title": "All ads", "book_ads": queryset, "links": temp_links}
    return render(request, template_name, context)


def get_ad_info(request, pk):
    template_name = 'ad_info.html'
    ad = BookAd.objects.get(pk=pk)
    temp_links = deepcopy(links)
    context = {"page_title": "Ad info", "ad": ad, "links": temp_links}
    return render(request, template_name, context)


class AdCreate(CreateView):
    model = BookAd
    fields = '__all__'


class AdUpdate(UpdateView):
    model = BookAd
    fields = '__all__'


class AdDelete(DeleteView):
    model = BookAd
    success_url = reverse_lazy('all-ads')

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import BookAd


def homePageView(request):
    return HttpResponse('Hello, World 2!')


def get_all_ads(request):
    template_name = 'all_ads.html'
    queryset = BookAd.objects.all()
    context = {"book_ads": queryset}
    return render(request, template_name, context)


def get_ad_info(request, pk):
    template_name = 'ad_info.html'
    ad = BookAd.objects.get(pk=pk)
    context = {"ad": ad}
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

from copy import deepcopy

from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import BookAd

links = [{"href": "/", "class": "item", "title": "صفحه اصلی"},
         {"href": "/ads", "class": "item", "title": "آگهی‌ها"},
         {"href": "/ads/new", "class": "item", "title": "ثبت آگهی"}]


def home_page_view(request):
    template_name = 'landing.html'  # 'index.html'
    temp_links = deepcopy(links)
    temp_links[0]["class"] = "active item"
    context = {"page_title": "کتاب‌باز - سامانه‌ی تبادل کتاب هوشمند", "links": temp_links}
    return render(request, template_name, context)


def get_all_ads(request):
    template_name = 'all_ads.html'
    queryset = BookAd.objects.filter(status=BookAd.AdStatus.ACCEPTED)
    temp_links = deepcopy(links)
    temp_links[1]["class"] = "active item"
    context = {"page_title": "کلیه‌ی آگهی‌ها", "book_ads": queryset, "links": temp_links}
    return render(request, template_name, context)


def update_ad_status(request, ad_id, accept):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied()
    add = get_object_or_404(BookAd, pk=ad_id)
    add.status = accept
    add.save()
    return HttpResponseRedirect(reverse('BookAdvertisement:all-pending-ads'))


def get_all_pending_ads_for_admin(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied()
    template_name = 'BookAdvertisement/ad_admin_accepting_list.html'
    queryset = BookAd.objects.filter(status=BookAd.AdStatus.PENDING)
    temp_links = deepcopy(links)
    temp_links[1]["class"] = "active item"
    context = {"page_title": "کلیه‌ی آگهی‌ها در در انتظار تایید", "book_ads": queryset, "links": temp_links}
    return render(request, template_name, context)


def get_ad_info(request, pk):
    template_name = 'ad_info.html'
    ad = get_object_or_404(BookAd, pk=pk)
    temp_links = deepcopy(links)
    context = {"page_title": "اطلاعات آگهی", "ad": ad, "links": temp_links}
    return render(request, template_name, context)


class AdCreate(CreateView):
    model = BookAd
    fields = ['poster', 'title', 'author', 'description', 'sell']

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj.owner = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())

    def get_context_data(self, **kwargs):
        ctx = super(AdCreate, self).get_context_data(**kwargs)
        temp_links = deepcopy(links)
        temp_links[2]["class"] = "active item"
        ctx['links'] = temp_links
        ctx["page_title"] = "آگهی جدید"
        ctx["nav"] = "آگهی جدید"
        return ctx


class AdUpdate(UpdateView):
    model = BookAd
    fields = ['poster', 'title', 'author', 'description', 'sell']

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.is_authenticated and obj.owner == self.request.user:
            obj.owner = self.request.user
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            raise PermissionDenied()

    def get_context_data(self, **kwargs):
        ctx = super(AdUpdate, self).get_context_data(**kwargs)
        temp_links = deepcopy(links)
        ctx['links'] = temp_links
        ctx["page_title"] = "ویرایش آگهی"
        ctx["nav"] = "ویرایش آگهی"
        return ctx


class AdDelete(DeleteView):
    model = BookAd
    success_url = reverse_lazy('all-ads')

    def get_context_data(self, **kwargs):
        ctx = super(AdDelete, self).get_context_data(**kwargs)
        temp_links = deepcopy(links)
        ctx['links'] = temp_links
        ctx["page_title"] = "delete ad"
        return ctx

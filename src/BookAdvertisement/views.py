from copy import deepcopy

from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import BookAd

links = [{"href": "/", "class": "item", "title": "صفحه اصلی"},
         {"href": "/ads", "class": "item", "title": "آگهی‌ها"},
         {"href": "/ads/new", "class": "item", "title": "ثبت آگهی"}]


def get_all_ads(request):
    filter_params = dict()
    for key in request.GET:
        attr = getattr(BookAd, key, None)
        if attr and isinstance(attr.field, models.IntegerField):
            filter_params[key] = int(request.GET[key])
        else:
            filter_params[key] = request.GET[key]

    template_name = 'all_ads.html'
    queryset = BookAd.objects.filter(status=BookAd.AdStatus.ACCEPTED) \
        .filter(**filter_params)
    temp_links = deepcopy(links)
    temp_links[1]["class"] = "active item"
    context = {"page_title": "کلیه‌ی آگهی‌ها", "book_ads": queryset, "links": temp_links}
    return render(request, template_name, context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_ad_status(request, ad_id, accept):
    add = get_object_or_404(BookAd, pk=ad_id)
    add.status = accept
    add.save()
    return HttpResponseRedirect(reverse('BookAdvertisement:all-pending-ads'))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_all_pending_ads_for_admin(request):
    template_name = 'BookAdvertisement/ad_admin_accepting_list.html'
    queryset = BookAd.objects.filter(status=BookAd.AdStatus.PENDING)
    temp_links = deepcopy(links)
    temp_links[1]["class"] = "active item"
    context = {"page_title": "کلیه‌ی آگهی‌ها در در انتظار تایید", "book_ads": queryset, "links": temp_links}
    return render(request, template_name, context)


def get_ad_info(request, pk):
    template_name = 'ad_info.html'
    ad: BookAd = get_object_or_404(BookAd, pk=pk)
    owner_score = ad.owner_score()
    temp_links = deepcopy(links)
    context = {"page_title": "اطلاعات آگهی", "ad": ad, "links": temp_links, "owner_score": owner_score}
    return render(request, template_name, context)


class AdCreate(CreateView):
    model = BookAd
    fields = ['poster', 'title', 'author', 'description', 'sell', 'suggested_money']

    def form_valid(self, form):
        from datetime import datetime, timezone
        # checking ad limit for user
        book_ads = BookAd.objects.filter(owner=self.request.user).order_by('created_datetime')
        now = datetime.now(timezone.utc)
        if book_ads.count() < 3 or (now - book_ads[book_ads.count() - 3].created_datetime).days > 30:
            from datetime import datetime
            obj: BookAd = form.save(commit=False)
            obj.owner = self.request.user
            obj.created_datetime = datetime.now()
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            # creation is not allowed
            title = "محدودیت آگهی"
            description = "سلام کاربر گرامی!" + "\n" + "هر کاربر در ماه تنها دسترسی به انتشار سه اگهی را دارد."
            link_redirect = ""
            return render(self.request, "BookAdvertisement/apply_information_page.html",
                          {'title': title, 'description': description, 'link_redirect': link_redirect})

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
    fields = ['poster', 'title', 'author', 'description', 'sell', 'suggested_money']

    def form_valid(self, form):
        from django.utils import timezone
        obj: BookAd = form.save(commit=False)
        if obj.owner == self.request.user:
            obj.owner = self.request.user
            obj.modified_datetime = timezone.datetime.now()
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
    success_url = reverse_lazy('BookAdvertisement:all-ads')

    def get_context_data(self, **kwargs):
        ctx = super(AdDelete, self).get_context_data(**kwargs)
        temp_links = deepcopy(links)
        ctx['links'] = temp_links
        ctx["page_title"] = "delete ad"
        return ctx

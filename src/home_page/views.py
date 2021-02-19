from copy import deepcopy

from django.shortcuts import render

links = [{"href": "/", "class": "item", "title": "صفحه اصلی"},
         {"href": "/ads", "class": "item", "title": "آگهی‌ها"},
         {"href": "/ads/new", "class": "item", "title": "ثبت آگهی"}]


# Create your views here.
def home_page_view(request):
    template_name = 'landing.html'  # 'index.html'
    temp_links = deepcopy(links)
    temp_links[0]["class"] = "active item"
    context = {"page_title": "کتاب‌باز - سامانه‌ی تبادل کتاب هوشمند", "links": temp_links}
    return render(request, template_name, context)

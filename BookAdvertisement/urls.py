from django.urls import path
from .views import homePageView, get_all_ads, get_ad_info



urlpatterns = [
    path('', homePageView, name='home'),
    path('ads/', get_all_ads),
    path('ads/<int:ad_id>/', get_ad_info),
]

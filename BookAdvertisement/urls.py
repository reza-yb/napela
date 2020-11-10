from django.urls import path
from .views import homePageView, get_all_ads, get_ad_info, AdCreate, AdUpdate, AdDelete

urlpatterns = [
    path('', homePageView, name='home'),
    path('ads/', get_all_ads, name='all-ads'),
    path('ads/<int:pk>/', get_ad_info, name='ad'),
    path('ads/<int:pk>/edit', AdUpdate.as_view(), name='ad-update'),
    path('ads/<int:pk>/delete', AdDelete.as_view(), name='ad-delete'),
    path('ads/new/', AdCreate.as_view(), name='ad-new'),
]

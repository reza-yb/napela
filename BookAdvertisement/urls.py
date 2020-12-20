from django.urls import path
from .views import home_page_view, get_all_ads, get_ad_info, AdCreate, AdUpdate, AdDelete, get_all_pending_ads_for_admin

urlpatterns = [
    path('', home_page_view, name='home'),
    path('ads/', get_all_ads, name='all-ads'),
    path('ads/pending/', get_all_pending_ads_for_admin, name='all--pending-ads'),
    path('ads/<int:pk>/', get_ad_info, name='ad'),
    path('ads/<int:pk>/edit', AdUpdate.as_view(), name='ad-update'),
    path('ads/<int:pk>/delete', AdDelete.as_view(), name='ad-delete'),
    path('ads/new/', AdCreate.as_view(), name='ad-new'),
]

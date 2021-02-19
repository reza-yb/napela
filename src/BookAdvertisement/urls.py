from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import get_all_ads, get_ad_info, AdCreate, AdUpdate, AdDelete, \
    get_all_pending_ads_for_admin, update_ad_status

app_name = 'BookAdvertisement'

urlpatterns = [
    path('', get_all_ads, name='all-ads'),
    path('pending/', get_all_pending_ads_for_admin, name='all-pending-ads'),
    path('pending/<int:ad_id>/<str:accept>/', update_ad_status, name='update-pending-ad-status'),
    path('<int:pk>/', get_ad_info, name='ad'),
    path('<int:pk>/edit', login_required(AdUpdate.as_view()), name='ad-update'),
    path('<int:pk>/delete', login_required(AdDelete.as_view()), name='ad-delete'),
    path('new/', login_required(AdCreate.as_view()), name='ad-new'),
]

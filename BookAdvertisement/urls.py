from django.urls import path
from .views import homePageView, get_all_ads



urlpatterns = [
    path('', homePageView, name='home'),
    path('ads/', get_all_ads),
    path('ads/<int:ad_id>/', views.get_single_event),
]

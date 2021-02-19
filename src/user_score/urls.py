from django.urls import path

from .views import set_advertisement_addresser_and_done

app_name = 'user_score'

urlpatterns = [
    path('set-addresser/<int:ad_id>/', set_advertisement_addresser_and_done, name='set_addresser_and_done'),
]

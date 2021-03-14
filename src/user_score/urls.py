from django.urls import path

from .views import set_advertisement_addresser_and_done, give_score

app_name = 'user_score'

urlpatterns = [
    path('set-addresser/<int:ad_id>/', set_advertisement_addresser_and_done, name='set_addresser_and_done'),
    path('give-score/<int:ad_id>/', give_score, name='give_score'),
]

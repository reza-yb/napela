from django.urls import path, reverse_lazy
from accounts import views
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/',
        RegistrationView.as_view(success_url=reverse_lazy('accounts:login')),
        name='register'),
    path('activate/<str:activation_key>/',
        ActivationView.as_view(success_url=reverse_lazy('accounts:login')),
        name="activate",
    ),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('profile/edit/', views.edit_profile_view, name='edit'),
    path('profile/my/', views.my_profile_view, name='my_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]

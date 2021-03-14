from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from BookAdvertisement.models import BookAd
from accounts.forms import ProfileForm, NamesForm
from accounts.models import Profile


@login_required
def my_profile_view(request):
    return redirect('accounts:profile', request.user.username)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    if hasattr(user, 'profile'):
        user_ads = user.bookad_set.all()
        score_ads = BookAd.objects.filter(addresser=user,status=BookAd.AdStatus.DONE)
        return render(request,
                      'accounts/profile.html',
                      {'target': user, 'user_ads': user_ads, 'score_ads': score_ads})
    elif request.user.is_authenticated and request.user.username == username:
        return redirect('accounts:edit')
    else:
        return HttpResponseNotFound()


@login_required
def edit_profile_view(request):
    if not hasattr(request.user, 'profile'):
        request.user.profile = Profile()

    profile_form = ProfileForm(request.POST or None, instance=request.user.profile)
    user_form = NamesForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        profile_valid = False
        user_valid = False

        if profile_form.is_valid():
            profile_valid = True
            profile = profile_form.save(commit=False)
            if request.user.profile is None:
                profile.user = request.user
            profile.save()

        if user_form.is_valid():
            user_valid = True
            user_form.save()

        if user_valid and profile_valid:
            return redirect('accounts:profile', username=request.user.username)

    return render(request, 'accounts/edit_profile.html', {'profile_form': profile_form, 'user_form': user_form})

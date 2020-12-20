from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def profile_view(request, username):
    pass


@login_required
def edit_profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    return render(request, 'accounts/profile.html', {'form': form})


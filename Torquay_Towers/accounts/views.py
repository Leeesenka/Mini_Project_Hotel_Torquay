from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .forms import ProfileForm
from django.contrib.auth.models import User

class ProfileView(DetailView):
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

def profile_redirect_view(request):

    user = request.user
    if hasattr(user, 'profile'):
        return redirect('profile-page', user.profile.id)
    else:
        return redirect('create-profile')

def create_profile_view(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_film')

    user = request.user
    form = ProfileForm(initial={'user': user})

    context = {'form': form}
    return render(request, 'create_profile.html', context)


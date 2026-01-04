from django.shortcuts import render, redirect

from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView

from .forms import RegisterForm, ProfileForm

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('main_page')
    return render(request, 'authorization/register.html', {'form': form})

def login_view(request):
    return LoginView.as_view(
        template_name='authorization/login.html'
    )(request)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('main_page')
    return render(request, 'authorization/profile_edit.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'authorization/dashboard.html')
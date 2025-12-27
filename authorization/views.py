from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'authorization/register.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'authorization/dashboard.html')

@login_required
def admin_view(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
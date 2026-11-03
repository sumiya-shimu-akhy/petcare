from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import Profile


def home(request):
    return render(request, 'accounts/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone'],
                area=form.cleaned_data['area'],
            )
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def check_username(request):
    username = request.GET.get('username', '').strip()
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'exists': exists})
import secrets
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import SignUpForm
from .models import Profile, EmailOTP


def home(request):
    return render(request, 'accounts/home.html')


def send_otp(user):
    code = f"{secrets.randbelow(1000000):06d}"
    otp, _ = EmailOTP.objects.get_or_create(user=user, defaults={'code': code})
    otp.code = code
    otp.save()
    send_mail(
        'Your Pet Care Finder verification code',
        f'Your verification code is {code}. It expires in 10 minutes.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def signup(request):
    if request.method == 'POST':
        User.objects.filter(is_active=False, username__iexact=request.POST.get('username', '').strip()).delete()
        User.objects.filter(is_active=False, email__iexact=request.POST.get('email', '').strip()).delete()
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone'],
                area=form.cleaned_data['area'],
            )
            send_otp(user)
            request.session['pending_user_id'] = user.id
            return redirect('verify_otp')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def verify_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('signup')
    user = get_object_or_404(User, pk=user_id)
    error = ''
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        otp = EmailOTP.objects.filter(user=user).first()
        if not otp or otp.is_expired():
            error = 'The code has expired. Please resend a new code.'
        elif otp.code != code:
            error = 'Wrong code. Please try again.'
        else:
            user.is_active = True
            user.save()
            otp.delete()
            del request.session['pending_user_id']
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    return render(request, 'accounts/verify_otp.html', {'error': error, 'email': user.email})


@require_POST
def resend_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('signup')
    user = get_object_or_404(User, pk=user_id)
    send_otp(user)
    return redirect('verify_otp')


def check_username(request):
    username = request.GET.get('username', '').strip()
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'exists': exists})
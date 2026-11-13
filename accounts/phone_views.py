import re
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import PhoneOTP, Profile, SmsLog
from .sms import send_sms

PHONE_RE = re.compile(r'^(?:\+?88)?(01[3-9]\d{8})$')
MAX_SENDS_PER_HOUR = 3
MAX_WRONG_TRIES = 5


def clean_phone(raw):
    raw = re.sub(r'[\s-]', '', raw or '')
    match = PHONE_RE.match(raw)
    return match.group(1) if match else None


def _profile(user):
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'role': 'owner'})
    return profile


@login_required
def phone_verify(request):
    profile = _profile(request.user)
    error = ''
    if request.method == 'POST':
        phone = clean_phone(request.POST.get('phone'))
        if not phone:
            error = 'Please enter a valid Bangladeshi mobile number, like 01712345678.'
        else:
            now = timezone.now()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            otp = PhoneOTP.objects.filter(user=request.user).first() or PhoneOTP(user=request.user)
            if otp.pk is None or now - otp.window_start > timedelta(hours=1):
                otp.window_start = now
                otp.sent_count = 0
            daily_limit = getattr(settings, 'SMS_DAILY_LIMIT', 50)

            if otp.sent_count >= MAX_SENDS_PER_HOUR:
                error = 'Too many codes requested. Please try again after an hour.'
            elif SmsLog.objects.filter(created_at__gte=start_of_day).count() >= daily_limit:
                error = "The site's daily SMS limit is reached. Please try again tomorrow."
            else:
                code = '%06d' % secrets.randbelow(1000000)
                sent = send_sms(phone, 'Your Pet Care Finder code is %s. It is valid for 10 minutes.' % code)
                if sent:
                    otp.phone = phone
                    otp.code = code
                    otp.attempts = 0
                    otp.sent_count += 1
                    otp.save()
                    SmsLog.objects.create()
                    return redirect('phone_confirm')
                error = 'Could not send the SMS. Please try again later.'

    return render(request, 'accounts/phone_verify.html', {
        'profile': profile,
        'error': error,
        'demo': getattr(settings, 'SMS_MODE', 'console') == 'console',
    })


@login_required
def phone_confirm(request):
    otp = PhoneOTP.objects.filter(user=request.user).first()
    if not otp:
        return redirect('phone_verify')
    error = ''
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        if otp.is_expired():
            error = 'The code has expired. Please request a new one.'
        elif otp.attempts >= MAX_WRONG_TRIES:
            error = 'Too many wrong tries. Please request a new code.'
        elif not secrets.compare_digest(code, otp.code):
            otp.attempts += 1
            otp.save(update_fields=['attempts'])
            error = 'Wrong code. Please try again.'
        else:
            profile = _profile(request.user)
            profile.phone = otp.phone
            profile.phone_verified = True
            profile.save()
            otp.delete()
            return redirect('phone_verify')
    return render(request, 'accounts/phone_confirm.html', {
        'error': error,
        'phone': otp.phone,
        'demo': getattr(settings, 'SMS_MODE', 'console') == 'console',
    })
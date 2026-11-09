import json
import time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .chat import ask_assistant


@login_required
def chat_page(request):
    return render(request, 'providers/chat.html')


@require_POST
def chat_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'reply': 'Please login to use the assistant.'}, status=403)

    now = time.time()
    recent = [t for t in request.session.get('chat_times', []) if now - t < 60]
    if len(recent) >= 8:
        return JsonResponse({'reply': 'Too many messages. Please wait a minute and try again.'}, status=429)
    recent.append(now)
    request.session['chat_times'] = recent

    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'reply': 'Invalid request.'}, status=400)
    message = str(data.get('message', '')).strip()[:500]
    if not message:
        return JsonResponse({'reply': 'Please type a message.'}, status=400)
    history = data.get('history', [])
    if not isinstance(history, list):
        history = []
    return JsonResponse({'reply': ask_assistant(message, history)})
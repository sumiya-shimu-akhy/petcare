from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Avg
from providers.models import ProviderProfile
from .models import Review


def reviews_json(request, provider_id):
    provider = get_object_or_404(ProviderProfile, pk=provider_id, is_verified=True)
    items = [
        {
            'user': r.user.username,
            'rating': r.rating,
            'comment': r.comment,
            'time': r.created_at.strftime('%d %b %Y, %I:%M %p'),
        }
        for r in provider.reviews.select_related('user')
    ]
    avg = provider.reviews.aggregate(a=Avg('rating'))['a']
    return JsonResponse({
        'reviews': items,
        'average': round(avg, 1) if avg else None,
        'count': len(items),
    })


@require_POST
def add_review(request, provider_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please login first'}, status=403)
    provider = get_object_or_404(ProviderProfile, pk=provider_id, is_verified=True)
    try:
        rating = int(request.POST.get('rating', ''))
    except ValueError:
        return JsonResponse({'error': 'Please choose a rating'}, status=400)
    comment = request.POST.get('comment', '').strip()
    if rating < 1 or rating > 5 or not comment:
        return JsonResponse({'error': 'Rating (1-5) and comment are required'}, status=400)
    Review.objects.create(provider=provider, user=request.user, rating=rating, comment=comment)
    return JsonResponse({'ok': True})
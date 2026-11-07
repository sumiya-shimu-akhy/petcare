from django.shortcuts import render

from .models import ProviderProfile
from .recommend import recommend


def provider_match(request):
    service = request.GET.get('service', '')
    area = request.GET.get('area', '').strip()
    budget_raw = request.GET.get('budget', '').strip()
    budget = int(budget_raw) if budget_raw.isdigit() else None
    searched = bool(request.GET)
    results = recommend(service, area, budget) if searched else []
    return render(request, 'providers/provider_match.html', {
        'results': results,
        'searched': searched,
        'service': service,
        'area': area,
        'budget': budget,
        'service_types': ProviderProfile.SERVICE_TYPES,
    })
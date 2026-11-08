import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ProviderForm
from .models import ProviderProfile


def distance_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


@login_required
def provider_edit(request):
    profile = ProviderProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            return redirect('provider_list')
    else:
        form = ProviderForm(instance=profile)
    return render(request, 'providers/provider_form.html', {'form': form})


def provider_list(request):
    providers = ProviderProfile.objects.filter(is_verified=True)
    service = request.GET.get('service', '')
    area = request.GET.get('area', '').strip()
    lat_raw = request.GET.get('lat', '')
    lng_raw = request.GET.get('lng', '')
    if service:
        providers = providers.filter(service_type=service)
    if area:
        providers = providers.filter(area__icontains=area)

    try:
        user_lat, user_lng = float(lat_raw), float(lng_raw)
        near = abs(user_lat) <= 90 and abs(user_lng) <= 180
    except ValueError:
        near = False

    if near:
        items = list(providers.select_related('user'))
        for p in items:
            if p.latitude is not None and p.longitude is not None:
                p.distance = round(distance_km(user_lat, user_lng, p.latitude, p.longitude), 1)
            else:
                p.distance = None
        items.sort(key=lambda p: (p.distance is None, p.distance or 0))
    else:
        items = providers.select_related('user').order_by('-id')

    paginator = Paginator(items, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'providers/provider_list.html', {
        'page_obj': page_obj,
        'service': service,
        'area': area,
        'near': near,
        'lat': lat_raw if near else '',
        'lng': lng_raw if near else '',
        'service_types': ProviderProfile.SERVICE_TYPES,
    })


def provider_detail(request, pk):
    provider = get_object_or_404(ProviderProfile, pk=pk, is_verified=True)
    return render(request, 'providers/provider_detail.html', {'provider': provider})
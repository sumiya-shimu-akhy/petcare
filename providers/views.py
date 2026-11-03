from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ProviderForm
from .models import ProviderProfile


@login_required
def provider_edit(request):
    profile = ProviderProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=profile)
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
    if service:
        providers = providers.filter(service_type=service)
    if area:
        providers = providers.filter(area__icontains=area)

    paginator = Paginator(providers.order_by('-id'), 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'providers/provider_list.html', {
        'page_obj': page_obj,
        'service': service,
        'area': area,
        'service_types': ProviderProfile.SERVICE_TYPES, 
    })
def provider_detail(request, pk):
    provider = get_object_or_404(ProviderProfile, pk=pk, is_verified=True)
    return render(request, 'providers/provider_detail.html', {'provider': provider})
from rest_framework import generics
from .models import ProviderProfile
from .serializers import ProviderSerializer


class ProviderListAPI(generics.ListAPIView):
    serializer_class = ProviderSerializer

    def get_queryset(self):
        qs = ProviderProfile.objects.filter(is_verified=True)
        service = self.request.query_params.get('service')
        area = self.request.query_params.get('area')
        if service:
            qs = qs.filter(service_type=service)
        if area:
            qs = qs.filter(area__icontains=area)
        return qs.order_by('-id')


class ProviderDetailAPI(generics.RetrieveAPIView):
    serializer_class = ProviderSerializer
    queryset = ProviderProfile.objects.filter(is_verified=True)
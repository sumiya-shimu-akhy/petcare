from django.contrib.auth.models import User
from providers.models import ProviderProfile

DEMO = [
    ('demo_vet', 'vet', 5, 1500, 'Chittagong'),
    ('demo_groomer', 'groomer', 2, 800, 'Dhaka'),
    ('demo_sitter', 'sitter', 3, 600, 'Chittagong'),
    ('demo_trainer', 'trainer', 4, 1200, 'Sylhet'),
]
for username, service, exp, fee, area in DEMO:
    user, _ = User.objects.get_or_create(username=username, defaults={'email': username + '@example.com'})
    ProviderProfile.objects.get_or_create(user=user, defaults=dict(
        service_type=service, experience_years=exp, fee=fee, area=area,
        bio='Demo provider for testing.', is_verified=True))
print('Demo providers ready')
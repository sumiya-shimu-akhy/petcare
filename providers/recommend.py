from django.db.models import Avg
from sklearn.neighbors import NearestNeighbors

from .models import ProviderProfile

# How much each preference matters
W_SERVICE, W_AREA, W_FEE, W_EXP, W_RATING = 3.0, 2.0, 1.5, 0.5, 1.0
# Largest possible distance, used to turn a distance into a 0-100 match score
MAX_DIST = (2 * W_SERVICE**2 + 2 * W_AREA**2 + W_FEE**2 + W_EXP**2 + W_RATING**2) ** 0.5


def recommend(service='', area='', budget=None, top_n=5):
    providers = list(
        ProviderProfile.objects.filter(is_verified=True)
        .select_related('user')
        .annotate(avg_rating=Avg('reviews__rating'))
    )
    if not providers:
        return []

    service_codes = [code for code, _ in ProviderProfile.SERVICE_TYPES]
    areas = sorted({p.area.strip().lower() for p in providers})
    max_fee = max(p.fee for p in providers) or 1
    max_exp = max(p.experience_years for p in providers) or 1

    typed = area.strip().lower()
    wanted = {a for a in areas if typed and (typed in a or a in typed)}

    def provider_vector(p):
        v = []
        v += [W_SERVICE if (service and p.service_type == code) else 0.0 for code in service_codes]
        v += [W_AREA if (wanted and p.area.strip().lower() == a) else 0.0 for a in areas]
        v += [max(0, p.fee - budget) / max_fee * W_FEE if budget else 0.0]
        v += [p.experience_years / max_exp * W_EXP]
        v += [(p.avg_rating or 0) / 5 * W_RATING]
        return v

    query = []
    query += [W_SERVICE if (service and code == service) else 0.0 for code in service_codes]
    query += [W_AREA if a in wanted else 0.0 for a in areas]
    query += [0.0]       # best case: nothing above the budget
    query += [W_EXP]     # prefer more experience
    query += [W_RATING]  # prefer a higher rating

    X = [provider_vector(p) for p in providers]
    k = min(top_n, len(providers))
    model = NearestNeighbors(n_neighbors=k).fit(X)
    distances, indexes = model.kneighbors([query])

    results = []
    for dist, i in zip(distances[0], indexes[0]):
        p = providers[i]
        reasons = []
        if service and p.service_type == service:
            reasons.append('Offers ' + p.get_service_type_display())
        if wanted and p.area.strip().lower() in wanted:
            reasons.append('Located in ' + p.area)
        if budget and p.fee <= budget:
            reasons.append('Within your budget (%s BDT)' % p.fee)
        if p.avg_rating:
            reasons.append('Rated %.1f / 5' % p.avg_rating)
        if p.experience_years:
            reasons.append('%s years experience' % p.experience_years)
        score = max(0, round(100 * (1 - float(dist) / MAX_DIST)))
        results.append({'provider': p, 'score': score, 'reasons': reasons})
    return results
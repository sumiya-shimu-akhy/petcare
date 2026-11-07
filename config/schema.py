import graphene
from django.db.models import Avg
from graphene_django import DjangoObjectType

from providers.models import ProviderProfile
from reviews.models import Review


class ProviderType(DjangoObjectType):
    username = graphene.String()
    average_rating = graphene.Float()
    review_count = graphene.Int()

    class Meta:
        model = ProviderProfile
        fields = ('id', 'service_type', 'experience_years', 'fee', 'area', 'bio')
        convert_choices_to_enum = False

    def resolve_username(self, info):
        return self.user.username

    def resolve_average_rating(self, info):
        avg = self.reviews.aggregate(a=Avg('rating'))['a']
        return round(avg, 1) if avg else None

    def resolve_review_count(self, info):
        return self.reviews.count()


class ReviewType(DjangoObjectType):
    username = graphene.String()

    class Meta:
        model = Review
        fields = ('id', 'rating', 'comment', 'created_at')

    def resolve_username(self, info):
        return self.user.username


class Query(graphene.ObjectType):
    providers = graphene.List(ProviderType, service=graphene.String(), area=graphene.String())
    provider = graphene.Field(ProviderType, id=graphene.Int(required=True))
    reviews = graphene.List(ReviewType, provider_id=graphene.Int(required=True))

    def resolve_providers(self, info, service=None, area=None):
        qs = ProviderProfile.objects.filter(is_verified=True).select_related('user')
        if service:
            qs = qs.filter(service_type=service)
        if area:
            qs = qs.filter(area__icontains=area)
        return qs.order_by('-id')

    def resolve_provider(self, info, id):
        return ProviderProfile.objects.filter(is_verified=True, pk=id).select_related('user').first()

    def resolve_reviews(self, info, provider_id):
        return Review.objects.filter(
            provider_id=provider_id, provider__is_verified=True
        ).select_related('user')


schema = graphene.Schema(query=Query)
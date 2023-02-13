from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from shoping_for_himself.models import *


class TitleForPeople(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticated,
                          )


class BrandForPeople(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated,
                          )


class OfferPeoples(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsAuthenticated,
                          )


class PriceTitle(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated,
                          )


class SizeTitle(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = (IsAuthenticated,
                          )


class ModelsTitle(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = ModelTitle.objects.all()
    serializer_class = ModelSerializer
    permission_classes = (IsAuthenticated,
                          )

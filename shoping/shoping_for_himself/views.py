# from http.client import HTTPResponse
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import *
from shoping_for_himself.models import *


class TitleForPeople(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductAll()
    permission_classes = (IsAuthenticated,
                          )


class BrandForPeople(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
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


class ListProduct(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated,
                          )

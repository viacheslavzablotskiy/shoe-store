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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticated,
                          )


class BrandForPeople(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated,
                          )


# class OfferPeoples(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin,
#                    viewsets.GenericViewSet):
#     queryset = Offer.objects.all()
#     serializer_class = OfferSerializer
#     permission_classes = (IsAuthenticated,
#                           )
# def get_item():
#     p = User.objects.values("username")
#     return p


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


class TitleList(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticated,
                          )

    # def post(self, request: Request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

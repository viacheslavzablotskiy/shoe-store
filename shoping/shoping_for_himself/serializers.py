from rest_framework import serializers
from .models import *


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ("size", "price",)


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTitle
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

from typing import Dict

from rest_framework import serializers
from .models import *


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ("size", "price",)


class TitleSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    size = serializers.ListField(
        child=serializers.ReadOnlyField(read_only=True)
    )

    class Meta:
        model = Title
        fields = ("model", "price", "brand", "title", "size")

    def create(self, validated_data: Dict):
        price_minimum = Price.objects.all().order_by("price")
        self.price = price_minimum
        return Title.objects.create(size=tuple(self.price),
                                    **validated_data)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


# class OfferSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Offer
#         fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTitle
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

# SizeSerializer(instance).data

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
        model = Product
        fields = ("model", "price", "brand", "name", "size")


class ProductAll(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'



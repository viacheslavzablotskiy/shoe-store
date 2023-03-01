from abc import ABC
from datetime import datetime
from typing import Dict

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm
from rest_framework import serializers
from .models import *


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Price
        fields = ["size", "price", "brand"]
        extra_kwargs = {
            'url': {'view_name': 'brand-detail'},
            'users': {'lookup_field': ''}
        }


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [Price(**item) for item in validated_data]
        return Price.objects.create(books)


class BookSerializer(serializers.ModelSerializer):
    poc = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='price-detail'
    )

    class Meta:
        model = Brand
        fields = ["brand", "poc", ]


class SetPassword(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class LoginSerializer(serializers.ModelSerializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
# create a object


# class BookSerializer(serializers.Serializer):
#     size = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=5, decimal_places=2)
#     brand = models.ForeignKey("Brand", null=True, blank=True, on_delete=models.SET_NULL)
#     # class CommentSerializer(serializers.Serializer):
#     #     email = serializers.EmailField()
#     #     content = serializers.CharField(max_length=200)
#     #     created = serializers.DateTimeField()
#
#     def create(self, validated_data):
#         return Price(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.size = validated_data.get('size', instance.size)
#         instance.price = validated_data.get('price', instance.price)
#         instance.brand = validated_data.get('brand', instance.brand)
#         return instance

# def get(self):
#     return Price.objects.all()

#
# class Comment(object):
#     def __init__(self, size, price, time=None):
#         self.email = size
#         self.content = price
#         self.created = time or datetime.now()
# class Meta:
#     model = Price
#     fields = ['size', "price"]
# def create(self, validated_data):
#     books = [Price(**item) for item in validated_data]
#     return Price.objects.create(books)

# def create(self, validated_data):
#     return Price(**validated_data)
# url = serializers.HyperlinkedIdentityField(
#     view_name='accounts',
#     lookup_field='slug'
# )
# users = serializers.HyperlinkedRelatedField(
#     view_name='user-detail',
#     lookup_field='username',
#     many=True,
#     read_only=True
# )

# class Meta:
#     model = Account
#     fields = ['url', 'account_name', 'users', 'created']

# class TitleSerializer(serializers.ModelSerializer):
#     price = serializers.DecimalField(max_digits=5, decimal_places=2)
#     size = serializers.ListField(
#         child=serializers.ReadOnlyField(read_only=True)
#     )
#
#     class Meta:
#         model = Product
#         fields = ("model", "price", "brand", "name", "size")
#
#
# class ProductAll(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"
#
#

#
#
# class SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Size
#         fields = '__all__'

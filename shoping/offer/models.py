from django.db import models
from datetime import date
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import  PermissionsMixin
from django.db.models import OuterRef, Subquery
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.reverse import reverse
import uuid
from rest_framework_simplejwt.tokens import RefreshToken


from django.conf import settings
from django.db import models
from offer.validators import validate_price


class StockBase(models.Model):
    code = models.CharField(max_length=10,
                            unique=True,
                            blank=False,)

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.code

    class Meta:
        abstract = True


class Currency(StockBase):
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Item(StockBase):
    currency = models.ForeignKey(
        Currency,
        related_name='+',
        on_delete=models.PROTECT,
        blank=False
    )


class Price(models.Model):
    value = models.FloatField(
        max_length=15,
        default=0

    )

    item = models.OneToOneField(
        Item,
        related_name='price',
        on_delete=models.CASCADE,
        blank=False
    )


class WatchList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watchlist',
        blank=False
    )

    items = models.ManyToManyField(
        Item
    )


class TradeBase(models.Model):
    price = models.FloatField(
        blank=False,
        validators=[validate_price]
    )

    amount = models.PositiveIntegerField(
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Offer(TradeBase):
    item = models.ForeignKey(
        Item,
        related_name='+',
        blank=False,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='offers',
        blank=False,
        on_delete=models.CASCADE
    )
    '''
    There are only to actions :
    Buy or Sell
    '''
    action = models.BooleanField(
        blank=False
    )


class Trade(TradeBase):
    item = models.ForeignKey(
        Item,
        related_name='+',
        blank=False,
        on_delete=models.SET_NULL,
        null=True,
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buy',
        blank=False,
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='sell',
        on_delete=models.CASCADE
    )


class Inventory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='inventory',
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='+',
        blank=False
    )

    amount = models.PositiveIntegerField(
        blank=False,
        default=0
    )

    '''It means these items wait for trade'''
    reserved_amount = models.PositiveIntegerField(
        blank=False,
        default=0
    )


class Account(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='accounts',
        on_delete=models.CASCADE
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='+'
    )

    balance = models.FloatField(
        default=0,
        validators=[validate_price]
    )

    '''It means this money wait for trade'''
    reserved_balance = models.FloatField(
        default=0,
        validators=[validate_price]
    )

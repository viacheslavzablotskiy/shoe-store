from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Title(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey('Brand', max_length=255, blank=True, null=True, on_delete=models.CASCADE)
    model = models.ForeignKey("ModelTitle", max_length=255, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}:{self.brand},{self.model}'


class Brand(models.Model):
    brand = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f'{self.brand}'


class Size(models.Model):
    title = models.ForeignKey("Title", max_length=255, null=True, blank=True, on_delete=models.CASCADE)
    size = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return f"{self.title}:{self.size}"


class ModelTitle(models.Model):
    model = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f"{self.model}"


class Price(models.Model):
    size = models.ForeignKey('Size', max_length=255, blank=True, null=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.price}{self.time}'


class Offer(models.Model):
    title = models.ForeignKey('Title', max_length=255, blank=True, null=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
    size = models.ForeignKey("Size", max_length=255, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} + {self.price}'

    def save(self, *args, **kwargs):
        price_this_pair = Price.objects.filter(size=self.size).order_by("price")
        price_this_pair = price_this_pair[0]
        self.price = price_this_pair.price
        super(Offer, self).save(*args, **kwargs)

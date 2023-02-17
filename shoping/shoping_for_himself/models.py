from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.db.models.signals import post_save
from django.dispatch import receiver


class Title(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey('Brand', max_length=255, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name="brand_title", related_query_name="brand_title")
    model = models.ForeignKey("ModelTitle", max_length=255, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name="model_title", related_query_name="model_title")

    def __str__(self):
        return f'{self.title}:{self.brand},{self.model}'

    def price(self):
        product = list(Title.objects.all())
        size = list(Size.objects.all())
        for product_number in product:
            product_number.size = list(Size.objects.filter(title_id=product_number.id))
            for price in product_number.size:
                price_min = list(Price.objects.filter(size_id=price).order_by("price"))
                price_min = price_min[0]
        return price_min.price

    def size(self):
        store = list(Title.objects.all())
        for shues in store:
            shues.size = list(Size.objects.filter(title_id=shues.id).values())
            shues.save()
            return shues.size


    #     .values("size",
        #                                                                                             "title_id"))
        #     fast = shues.size
        # return fast


# hero_qs = Hero.objects.filter(
#     category=OuterRef("pk")
# ).order_by("-benevolence_factor")
# Category.objects.all().annotate(
#     most_benevolent_hero=Subquery(
#         hero_qs.values('name')[:1]
#     )
class Brand(models.Model):
    brand = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f'{self.brand}'


class Size(models.Model):
    title = models.ForeignKey("Title", max_length=255, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="title_size", related_query_name="title_size")
    size = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return f"title:{self.title}"
        # f"price:{self.size}"


class ModelTitle(models.Model):
    model = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f"{self.model}"


class Price(models.Model):
    size = models.ForeignKey('Size', max_length=255, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name="price_size", related_query_name="price_size")
    price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.price}{self.time}'

# class Offer(models.Model):
#     title = models.ForeignKey('Title', max_length=255, blank=True, null=True, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=5, decimal_places=2, max_length=5, null=True, blank=True)
#     size = models.ForeignKey("Size", max_length=255, null=True, blank=True, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.title} + {self.price}'
#
#     def save(self, *args, **kwargs):
#         price_this_pair = Price.objects.filter(size=self.size).order_by("price")
#         price_this_pair = price_this_pair[0]
#         self.price = price_this_pair.price
#         super(Offer, self).save(*args, **kwargs)

from django.contrib import admin
from offer.models import *


# Register your models here.
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # price = Price.objects.create(item=obj)


admin.site.register(Inventory)
admin.site.register(Price)
admin.site.register(WatchList)
admin.site.register(Trade)
admin.site.register(Offer)
admin.site.register(Account)

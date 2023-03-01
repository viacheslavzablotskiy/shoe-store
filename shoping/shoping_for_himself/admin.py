from django.contrib import admin
from rest_framework_simplejwt.tokens import OutstandingToken
from .models import *


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.register(User)
admin.site.register(Price)
admin.site.register(Room)
admin.site.register(Brand)
admin.site.register(Message)
admin.site.register(Profile)

from django.contrib import admin
from rest_framework_simplejwt.tokens import OutstandingToken
from .models import *


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]


admin.site.register(User)
admin.site.register(Track)
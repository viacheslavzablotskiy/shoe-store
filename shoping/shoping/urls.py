from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from shoping_for_himself import views
from shoping_for_himself.views import *
from django.contrib import admin
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"title", TitleForPeople),
router.register(r"brand", BrandForPeople),
router.register(r"size", SizeTitle),
router.register(r"lis", ListProduct)
router.register(r"price", PriceTitle),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/login/', include("rest_framework.urls")),
]
urlpatterns += router.urls

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView


from rest_framework import views
from shoping_for_himself.views import *
from django.contrib import admin
from django.urls import path, include, re_path

router = routers.DefaultRouter()
# router.register(r"title", TitleForPeople),
# router.register(r"brand", BrandForPeople),
# router.register(r"size", SizeTitle),
# router.register(r"brand", ListProduct)
# router.register(r"price", PriceTitle),
# router.register(r"named", Profile_list),
# router.register("price_brand", SizeTitle , basename="lod")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('dwitter', dashboard),

    # path("profile_list/", profile_list, name="profile_list"),
    # path("profiles/<int:pk>", profile, name="profile"),
    # path('auth/', include('authentication.urls')),
    # re_path('social-auth/', include('social_django.urls', namespace="social")),
    # path('channel', index_view, name='chat-index'),
    # path('<str:room_name>/', room_view, name='chat-room'),
    # path('accounts/', include('allauth.urls')),
    # path('api/auth/', include('djoser.urls')),
    # path('table', setsession),
    # path('desk', updating_cookie),
    # path('oil', getsession),
    # path('cookie', setcookie),
    # # path('kok', login),
    # path('login', LoginView.as_view()),
    # path('get_user', ExampleView.as_view()),
    # # path('google/', views.GoogleLogin.as_view(), name='google_login'),
    # path("password", views.change_password, name="password_change"),
    # path("password_reset", password_reset_request, name="password_reset"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/login/', include("rest_framework.urls")),
    path("login/", include("shoping_for_himself.urls"))
    # path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += router.urls

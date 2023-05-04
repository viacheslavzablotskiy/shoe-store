from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


from shoping_for_himself.views import RegistrationAPIView, LoginAPIView, LogoutAPIView, UserRetrieveUpdateAPIView, \
    PostList, LoginUser, UpdateUser, TrackView, example, loginn, total, news_home, create_track, NewDetails

# router = routers.DefaultRouter()
# router.register(r"track", TrackView),

urlpatterns = [
                  path("<int:pk>", NewDetails.as_view(), name="login-details"),
                  path("create", create_track, name="create_truck"),
                  path('total', total, name="total_truck"),
                  path("now", news_home, name="new_news"),
                  path("login", loginn, name="login_template"),
                  path("example", example, name="example_tasks"),
                  # path("track", Track.as_view({'get': 'list', 'post': 'create'})),
                  path('me/', UpdateUser.as_view({'get': 'retrieve', 'put': 'update'})),
                  path("register_user", PostList.as_view(), name="register_user"),
                  path("login_user", LoginUser.as_view(), name="login_user"),
                  path('register/', RegistrationAPIView.as_view(), name='register_user'),
                  path('login/', LoginAPIView.as_view(), name='login_user'),
                  path('logout/', LogoutAPIView.as_view(), name="logout_user"),
                  path('user/', UserRetrieveUpdateAPIView.as_view(), name='user'),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += router.urls

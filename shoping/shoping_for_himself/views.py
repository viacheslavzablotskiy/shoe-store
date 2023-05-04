# from http.client import HTTPResponse
import time
from typing import Any

from django.views.generic import DetailView

from .forms import TrackForm
from rest_framework.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Subquery, Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import mixins, viewsets, status, request, permissions, views, generics, parsers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import *
from shoping_for_himself.serializers import LoginSerializer
from shoping_for_himself.models import *
from django.utils.translation import gettext_lazy

from rest_framework.response import Response


def loginn(request):
    """ Страница входа через Google
    """
    data = "Hello"
    news = User.objects.all()
    return render(request, 'login.html', {"title": "ghbdtn"})


def news_home(request):
    return render(request, "new_news.html")


class NewDetails(DetailView):
    model = User
    template_name = "my_truck.html"
    context_object_name = "article"


def create_track(request):
    error = ''
    if request.method == "POST":
        form = TrackForm(request.POST)
        # if request.user.is_authenticated():
        if form.is_valid():
            new_posts = form.save(commit=False)
            new_posts.user = request.user
            new_posts.save()
            return redirect("login_template")
        else:
            error = "Form is not correct"
        # else:
        #     raise

    form = TrackForm()

    data = {
        "form": form,
        "error": error
    }
    return render(request, "truck.html", data)


def example(request):
    """ Страница входа через Google
    """
    news = User.objects.all()
    return render(request, 'example.html', {"news": news})


def total(request):
    """ Страница входа через Google
    """

    return render(request, 'total.html')


class PostList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(user=user)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUser(viewsets.ModelViewSet):
    """ Просмотр и редактирование данных пользователя
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.username
        my_models = User.objects.filter(username=user)

        if my_models.exists():
            my_models = my_models[0]
            return my_models

    def get_object(self):
        return self.get_queryset()

    # def update(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]) -> Response:
    #     """Return updated user."""
    #     serializer_data = request.data.get('user', {})
    #
    #     serializer = self.serializer_class(
    #         request.user, data=serializer_data, partial=True, context={'request': request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]) -> Response:
        """Return user on GET request."""
        serializer = self.serializer_class(request.user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]) -> Response:
        """Return updated user."""
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TrackView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializers
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Track.objects.filter(user=user)

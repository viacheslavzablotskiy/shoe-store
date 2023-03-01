# from http.client import HTTPResponse
import time

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
from rest_framework import mixins, viewsets, status, request, permissions, views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from shoping_for_himself.serializers import LoginSerializer
from shoping_for_himself.models import *
from django.utils.translation import gettext_lazy

from rest_framework.response import Response


def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    # return HttpResponse(f"{profile}")

    return render(request, "profile.html", {"profile": profile})


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "profile_list.html", {"profiles": profiles})


def dashboard(request):
    return render(request, "base.html")


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })


# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView
#
#
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter


class PriceTitle(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    queryset = Price.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = (IsAuthenticated,
                          )


class Profile_list(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated,
                          )


class ListProduct(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated,
                          )

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.count = obj.count + 1
        obj.save(update_fields=("count",))
        return super().retrieve(request, *args, **kwargs)


#

class SizeTitle(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,
                          )

    def create(self, request):
        user = request.user
        send_mail('Verify your QuickPublisher account',
                  'Follow this link to verify your account: '
                  'http://localhost:8000%s' % reverse("price-list"),
                  'zlava.mag@gmail.com',
                  [user.email],
                  fail_silently=False,
                  )
        return HttpResponse("привет")


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return redirect("password_change")

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    # email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    try:
                        send_mail(subject, c, 'zlava.mag@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return redirect("password_reset")


def setsession(request):
    request.session['username'] = 'irfan'
    request.session['email'] = 'irfan.sssit@gmail.com'
    return HttpResponse("session is set")


def updating_cookie(request):
    html = HttpResponse("We are updating  the cookie which is set before")
    html.set_cookie('JavaTpoint', 'Updated Successfully')
    return html


def getsession(request):
    studentname = request.session['username']
    studentemail = request.session['email']
    return HttpResponse(studentname + " " + studentemail)


def setcookie(request):
    time.sleep(10)
    html = HttpResponse("<h1>Dataflair Django Tutorial</h1>")
    if request.COOKIES.get('visits'):
        html.set_cookie('dataflair', 'Welcome Back')
        value = int(request.COOKIES.get('visits'))
        html.set_cookie('visits', value + 1)
    else:
        value = 1
        text = "Welcome for the first time"
        html.set_cookie('visits', value)
        html.set_cookie('dataflair', text)
    return html


def showcookie(request):
    if request.COOKIES.get('visits') is not None:
        value = request.COOKIES.get('visits')
        text = request.COOKIES.get('dataflair')
        html = HttpResponse(
            "<center><h1>{0}<br>You have requested this page {1} times</h1></center>".format(text, value))
        html.set_cookie('visits', int(value) + 1)
        return html
    else:
        return redirect('setcookie')


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

# def login(request):
#     if request.method != 'POST' and request.method != 'GET':
#         raise Http404('Only POSTs are allowed')
#     try:
#         m = User.objects.get(username=request.POST['username'])
#         if m.password == request.POST['password']:
#             request.session['member_id'] = m.id
#             return HttpResponseRedirect('/you-are-logged-in/')
#     except User.DoesNotExist:
#         return HttpResponse("Your username and password didn't match.")
# # @login_required
# def password_change(request):
#     user = request.user
#     form = SetPasswordForm(user)
#     return form
#
#     def get(self):
#         return SetPassword.objects.all()
#
#

# class TitleForPeople(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductAll()
#     permission_classes = (IsAuthenticated,
#                           )
#
#
# class BrandForPeople(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer
#     permission_classes = (IsAuthenticated,
#                           )

import os
from django.contrib.auth.models import BaseUserManager
from account.scripts import generate_token, get_domain
from account.tasks import send_mail_task
from rest_framework.reverse import reverse
from account.signals import user_created


class UserManager(BaseUserManager):

    def _send_confirm_link_on_mail(self, user):
        token = generate_token(pk=user.pk)
        link = get_domain() + reverse('activate-detail', args=[token])

        message = "Dear, {}. In order to activate your account folow" \
                  "this link: {}".format(user, link)

        send_mail_task.delay(
            'Confirmation email',
            message,
            os.environ.get("EMAIL_HOST_USER"),
            [user.email])

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError("Username is required!")

        if not email:
            raise ValueError("Email is required!")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        user_created.send(
            sender=user.__class__,
            instance=user
        )

        self._send_confirm_link_on_mail(user)

        return user

    def create_user(self, username, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_staff for superuser should bet True!")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser for superuser should bet True!")

        return self._create_user(username, email, password, **extra_fields)

from datetime import date
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.db.models import OuterRef, Subquery
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.reverse import reverse

import uuid

from rest_framework_simplejwt.tokens import RefreshToken


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(null=True)
    full_name = models.CharField(max_length=20000, null=True)
    birth_date = models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserAccountManager()

    def __str__(self) -> str:
        """Return a string representation of this `User`."""
        string = self.email if self.email != '' else self.get_full_name()
        return f'{self.email} {string}'

    @property
    def tokens(self) -> dict[str, str]:
        """Allow us to get a user's token by calling `user.token`."""
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def get_full_name(self) -> Optional[str]:
        """Return the full name of the user."""
        return self.full_name

    def get_short_name(self) -> str:
        """Return user username."""
        return self.username


class Track(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

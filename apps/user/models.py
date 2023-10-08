from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, first_name, last_name, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,  # Include any additional fields as keyword arguments
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    first_name = models.CharField(max_length=100, unique=False, blank=False, null=False)
    last_name = models.CharField(max_length=100, unique=False, blank=False, null=False)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    password = models.CharField(max_length=100, unique=False, blank=False, null=False)
    subscribed = models.BooleanField(
        default=False
    )  # if they are a paid user, can make a profit off the app
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=100, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"] # when creating super users, this is what will be prompted on the CLI


class Blogger(User):
    pass


class Photographer(User):
    pass

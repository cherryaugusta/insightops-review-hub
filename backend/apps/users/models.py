from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return self.username

    @property
    def display_name(self) -> str:
        full_name = self.get_full_name().strip()
        return full_name or self.username

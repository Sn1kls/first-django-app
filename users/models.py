from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=50, blank=True)
    house_number = models.CharField(max_length=10, blank=True)
    street = models.CharField(max_length=100, blank=True)
    is_doctor = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "phone_number", "city"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

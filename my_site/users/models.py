from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField()
    password = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    region = models.CharField(max_length=30, blank=False)
    house_number = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=30, blank=True)
    is_doctor = models.BooleanField(default=False)


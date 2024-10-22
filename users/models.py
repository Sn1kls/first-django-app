from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    house_number = models.CharField(max_length=10, blank=True)
    street = models.CharField(max_length=100, blank=True)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_resident = models.BooleanField(default=True)
    is_lgu_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        role = "Staff" if self.is_lgu_staff else "Resident"
        return f"{self.email}: {role}"
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser


class Userviber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    viber_id = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=15, null=True)
    country = models.CharField(max_length=15, null=True)
    phone_number = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=True, null=True)
    is_bloked = models.BooleanField(default=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    def str(self):
        return f'{self.name} - {self.phone_number}'
# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class UserOne(AbstractUser):
    Job_position = models.ForeignKey('JobPosition', on_delete=models.PROTECT, null=True, blank=True, related_name='user_job')


class JobPosition(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'
# Create your models here.

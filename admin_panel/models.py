# adminapp/models.py

from django.db import models
from django.conf import settings


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add additional fields specific to admin

    def __str__(self):
        return self.user.username

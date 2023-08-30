from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    display_name = models.CharField(max_length=32, blank=True)
    # Add more fields for user profile information if needed

    def __str__(self):
        return self.username





from django.contrib.auth.models import User
from django.db import models


class DbUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_number = models.IntegerField(
        primary_key=True, au
        unique=True, blank=False, null=False)

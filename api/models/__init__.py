from .node import Node
from .link import Link
from .segment import Segment
from .traveltime import TravelTime

# from django.contrib.auth.models import User
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# for user in User.objects.all():
#     print("Running")
#     Token.objects.get_or_create(user=user)

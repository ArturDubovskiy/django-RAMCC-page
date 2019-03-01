from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify


class JoinClub(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(auto_now_add=False, auto_now=False, blank=False)



from django.db import models
from uuid import uuid4


class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=50, unique=True)
    session_token = models.CharField(max_length=50, default=0)
    reset_token = models.CharField(max_length=50, default=0)
    activation_token = models.CharField(max_length=50, default=str(uuid4))
    activated = models.BooleanField(default=False)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

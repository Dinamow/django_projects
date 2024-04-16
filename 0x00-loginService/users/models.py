""" This module contains the Users model. """
from django.db import models


class Users(models.Model):
    """Users model"""
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=50, unique=True)
    session_token = models.CharField(max_length=50, null=True, blank=True)
    reset_token = models.CharField(max_length=50, null=True, blank=True)
    activation_token = models.CharField(max_length=50, unique=True)
    activated = models.BooleanField(default=False)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """Return dictionary representation of the model."""
        return {'username': self.username,
                'email': self.email,
                'phone': self.phone,
                'address': self.address,
                'city': self.city,
                'state': self.state,
                'country': self.country,
                'zip': self.zip,
                'last_update': self.updated_at}

    def __str__(self):
        """Return string representation of the model."""
        return self.username

from django.urls import path
from users.views import *


urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('users_count/', users_count, name='users_count'),
    path('all_users/', all_users, name='all_users'),
]
from django.urls import path
from users.views import *


urlpatterns = [
    path('', working_app, name='working_app'),
    path('signup/', create_user, name='signup'),
    path('activate/', activate_user, name='activate'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('all_users/', all_users, name='all_users'),
]
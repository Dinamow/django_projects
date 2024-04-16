from django.urls import path
from users.views import *


urlpatterns = [
    path('signup/', create_user, name='signup'),
    path('activate/', activate_user, name='activate'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('<str:username>', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('delete_acc/', delete_acc, name='delete_acc')
]
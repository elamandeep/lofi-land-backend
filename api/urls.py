from django.urls import path , include
from .views import *

urlpatterns=[
#  path("musiclist/", get_music , name="musiclist"),
 path("environments/", get_environment , name='environments'),
 path("auth/", get_or_create_user, name="auth"),
 path("logout/", logout_user, name="logout"),
]
from django.urls import include, path
from .views import *

urlpatterns = [
    path('hello/', hello, name='hello'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('secret/', secret, name='secret'),
    path('tweets/', tweets_list, name='tweets_list'),
]
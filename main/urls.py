from django.urls import include, path
from .views import index
from .views import hello

urlpatterns = [
    path('', index, name='index'),
    path('hello/', hello, name='hello'),
]
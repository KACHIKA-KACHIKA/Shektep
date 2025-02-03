from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', test_creation_page, name='tests'),
    path('test/', test, name='test'),
]

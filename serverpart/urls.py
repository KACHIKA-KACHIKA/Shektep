from django.urls import path
from .views import test, test_creation_page

urlpatterns = [
    path('', test_creation_page, name='tests'),
    path('test/', test, name='test'),
]

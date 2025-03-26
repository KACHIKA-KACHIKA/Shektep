from django.urls import path
from .views import exams, examing, result
urlpatterns = [
    path('', exams, name='exams'),
    path('examing/', examing, name='examing'),
    path('result/', result, name='result'),
]

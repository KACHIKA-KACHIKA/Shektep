from django.urls import path
from .views import *
urlpatterns = [
	path('', exams, name='exams'),
	path('examing/', examing, name='examing'),
	path('result/', result, name='result'),
]
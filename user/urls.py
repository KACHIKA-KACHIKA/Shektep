from django.urls import path
from django.views.generic.base import RedirectView

from .views import *
urlpatterns = [
	path('signup/', signupuser, name='signup'),
	path('logout/', logoutuser, name='logout'),
	path('login/', loginuser, name='login'),
	# path('signup/', RedirectView.as_view(url='/'), name='signup'),
	# path('logout/', RedirectView.as_view(url='/'), name='logout'),
	# path('login/', RedirectView.as_view(url='/'), name='login'),
]
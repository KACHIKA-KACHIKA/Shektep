from django.urls import path

from .views import signupuser, logoutuser, loginuser
urlpatterns = [
    path('signup/', signupuser, name='signup'),
    path('logout/', logoutuser, name='logout'),
    path('login/', loginuser, name='login'),
]

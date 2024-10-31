from django.shortcuts import get_object_or_404, render, redirect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

def signupuser(request):
	if request.method == 'GET':
			return render(request, './signup.html', {'form': UserCreationForm()})
	else:
			if request.POST['password1'] == request.POST['password2']: 
					try:
							_user = User.objects.create_user(request.POST['username'],password=request.POST['password2'])
							_user.save()
							login(request, _user)
							return redirect('home')
					except IntegrityError:
							return render(request, './signup.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})

			else:
					return render(request, './signup.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def logoutuser(request):
		if request.method == 'POST':
				logout(request)
				return redirect('home')

def loginuser(request):
		if request.method == 'GET':
				return render(request, './login.html',{'form': AuthenticationForm()})
		else:
				user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
				if user is None:
						return render(request, './login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
				else:
						login(request, user)
						return redirect('home')
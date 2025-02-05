from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django_ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='5/m', block=True)
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        username = request.POST['username']
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Пароли не совпадают',
                'username': username,
                'first_name': first_name,
                'second_name': second_name,
            })

        try:
            validate_password(password1)  # Валидация пароля
            _user = User.objects.create_user(
                username=username,
                password=password2,
                first_name=first_name,
                last_name=second_name
            )
            _user.save()
            login(request, _user)
            return redirect('home')
        except ValidationError as e:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': ' '.join(e.messages),
                'username': username,
                'first_name': first_name,
                'second_name': second_name,
            })
        except IntegrityError:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'Этот никнейм уже занят, выберите, пожалуйста, другой.',
                'username': username,
                'first_name': first_name,
                'second_name': second_name,
            })


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('landing')


def loginuser(request):
    if request.method == 'GET':
        return render(request, './login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, './login.html', {'form': AuthenticationForm(), 'error': 'Никнейм и пароль не сходятся'})
        else:
            login(request, user)
            return redirect('home')

from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.contrib.auth import login, logout, views as auth_views, authenticate
from hotex_app.forms import LoginForm

def login_page(request):

  #Redirect to dashboard if user is authenticated
  if request.user.is_authenticated:
    return redirect('/')

  #Authenticate user
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if not form.is_valid():
      return render(request, 'login.html', {'form': form})

    cleaned_data = form.cleaned_data
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      messages.error(request, 'Invalid username or password.')
      return render(request, 'login.html', {'form': form})

  #If the user is not authenticated show login form
  form = LoginForm()
  return render(request, 'login.html', {'form': form})

def terminate_session(request):
  logout(request)
  return redirect('login')

urlpatterns = [
  path('login/', login_page, name='login'),
  path('logout/', terminate_session, name='logout')
]

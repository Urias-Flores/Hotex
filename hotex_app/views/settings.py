from django.shortcuts import render
from django.urls import path

def settings_page(request):
  return (render(
    request,
    'settings.html',
    {
      'user': request.user,
      'title': 'Settings',
      'current_path': request.path
    }))

urlpatterns = [
    path('', settings_page, name='settings'),
]
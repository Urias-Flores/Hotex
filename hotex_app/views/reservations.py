from datetime import datetime

from django.shortcuts import render
from django.urls import path

from hotex_app.forms import ReservationForm
from hotex_app.models import Reservation, Room, Guest
from urllib.parse import unquote

def reservations_page(request):
  reservations = Reservation.objects.all()
  rooms = Room.objects.all()
  room = int(request.GET.get('room', 0))
  date = request.GET.get('date', '')
  search = unquote(request.GET.get('search', ''))

  if room != 0:
    reservations = reservations.filter(room__id=room)

  if date != '':
    _date = datetime.strptime(date, '%Y-%m-%d').date()
    reservations = reservations.filter(check_in__lte=_date, check_out__gt=_date)

  if search != '':
    reservations = reservations.filter(guest__name__contains=search)

  return (render(
    request,
    'reservations.html',
    {
      'user': request.user,
      'title': 'Reservations',
      'current_path': request.path,
      'reservations': reservations,
      'rooms': rooms,
      'query_params': {
        'room': room,
        'date': date,
        'search': search
      }
    }))

def add_reservation_page(request):
  return render(
    request,
    'forms/reservation_form.html',
    {
      'user': request.user,
      'title': 'Add Reservation',
      'current_path': request.path,
      'rooms': Room.objects.all(),
      'guests': Guest.objects.all(),
      'form': ReservationForm
    })

urlpatterns = [
    path('', reservations_page, name='reservations'),
    path('new/', add_reservation_page, name='add-reservation'),
]
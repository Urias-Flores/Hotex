from django.shortcuts import render
from django.urls import path
from django.contrib.auth.decorators import login_required
from datetime import datetime
import calendar as cal

from hotex_app.models import Room, Reservation, Maintenance

@login_required(login_url='login')
def dashboard_page(request):
  today: datetime = datetime.now()

  arrivals = Reservation.objects.filter(
    check_in__year=today.year,
    check_in__month=today.month,
    check_in__day=today.day
  ).count()

  departures = Reservation.objects.filter(
    check_out__year=today.year,
    check_out__month=today.month,
    check_out__day=today.day
  ).count()

  rooms = Room.objects.all()
  for index, room in enumerate(rooms):
    room.is_available = not (
        Reservation
        .objects
        .filter(room__id=room.id, check_in__lte=today, check_out__gt=today).exists()
        or
        Maintenance
        .objects
        .filter(room__id=room.id, start_date__lte=today, end_date__gt=today).exists()
    )

  room = int(request.GET.get('room', rooms.first().id))
  year = request.GET.get('year', today.year)
  month = request.GET.get('month', today.month)

  try:
    year = int(year)
    month = int(month)
  except (ValueError, TypeError):
    year = today.year
    month = today.month

  cal_data = cal.monthcalendar(year+1, month)
  month_name = cal.month_name[month]

  reservation_list = []
  reservations = Reservation.objects.filter(
    room=room,
    check_in__year=year,
    check_in__month=month
  )

  for reservation in reservations:
    reservation_list.append([day for day in range(reservation.check_in.day, reservation.check_out.day + 1)])

  return (render(
    request,
    'dashboard.html',
    {
      'user': request.user,
      'title': 'Dashboard',
      'current_path': request.path,
      'calendar_days': cal_data,
      'month': month,
      'month_name': month_name,
      'year': year,
      'current_day': today.day,
      'current_month': today.month,
      'next_month': month + 1 if month < 12 else 1,
      'previous_month': month - 1 if month > 1 else 12,
      'current_year': today.year,
      'next_year': year + 1 if month == 12 else year,
      'previous_year': year - 1 if month == 1 else year,
      'reservations': reservation_list,
      'rooms': rooms,
      'arrivals': arrivals,
      'departures': departures,
      'query_data': {
        'month': month,
        'year': year,
        'room': room
      }
    }))

urlpatterns = [
  path('', dashboard_page, name='dashboard'),
]
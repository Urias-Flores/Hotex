from django.shortcuts import render
from django.urls import path
from django.db.models import Count
from hotex_app.models import Room, Building, Maintenance
from hotex_app.forms import RoomForm, BuildingForm, MaintenanceForm

def rooms_page(request):
  return (render(
    request,
    'rooms.html',
    {
      'user': request.user,
      'title': 'Rooms',
      'current_path': request.path,
      'rooms': Room.objects.all()
    }))

def add_room_page(request):
  return render(
    request,
    'forms/room_form.html',
    {
      'user': request.user,
      'title': 'Add Room',
      'current_path': request.path,
      'form': RoomForm
    })

def update_room(request, room_id):

  # setting room to be edited
  room = Room.objects.get(id=room_id)
  form = RoomForm()
  form.fields['id'].initial = room.id
  form.fields['number'].initial = room.number
  form.fields['type'].initial = room.type
  form.fields['building'].initial = room.building
  form.fields['floor'].initial = room.floor
  form.fields['persons'].initial = room.persons
  form.fields['beds'].initial = room.beds

  return render(
    request,
    'forms/room_form.html',
    {
      'user': request.user,
      'title': 'Edit Room',
      'current_path': request.path,
      'form': form,
      'room': room
    })

def buildings_page(request):
  buildings = Building.objects.annotate(rooms_count=Count('room')).order_by('name')
  building = int(request.GET.get('building', 0))

  return (render(
    request,
    'buildings.html',
    {
      'user': request.user,
      'title': 'Buildings',
      'current_path': request.path,
      'buildings': buildings,
      'query_params': {
        'building': building
      }
    }))

def add_building_page(request):
  return render(
    request,
    'forms/building_form.html',
    {
      'user': request.user,
      'title': 'Add Building',
      'current_path': request.path,
      'form': BuildingForm
    })

def maintenance_page(request):
  return (render(
    request,
    'maintenances.html',
    {
      'user': request.user,
      'title': 'Maintenance',
      'current_path': request.path,
      'maintenances': Maintenance.objects.all()
    }))

def add_maintenance_page(request):
  return render(
    request,
    'forms/maintenance_form.html',
    {
      'user': request.user,
      'title': 'Add Maintenance',
      'current_path': request.path,
      'form': MaintenanceForm,
    })

urlpatterns = [
    path('', rooms_page, name='rooms'),
    path('new/', add_room_page, name='add-room'),
    path('edit/<int:room_id>', update_room, name='edit-room'),
    path('buildings/', buildings_page, name='buildings'),
    path('buildings/new/', add_building_page, name='add-building'),
    path('maintenance/', maintenance_page, name='maintenances'),
    path('maintenance/new/', add_maintenance_page, name='add-maintenance'),
]
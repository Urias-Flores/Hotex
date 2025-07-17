from django.shortcuts import redirect, render
from django.urls import path
from hotex_app.models import Reservation, Guest, Room, Building, Maintenance
from django.contrib import messages
from hotex_app.forms import ReservationForm, GuestForm, RoomForm, BuildingForm, MaintenanceForm

def add_reservation(request):
  if request.method != 'POST':
    messages.error(request, "Method not allowed.")
    return redirect('add-reservation')

  form = ReservationForm(request.POST)

  if not form.is_valid():
    return render(
      request,
      'forms/reservation_form.html',
      {
        'username': 'John Doe',
        'position': 'Manager',
        'title': 'Add Reservation',
        'current_path': request.path,
        'rooms': Room.objects.all(),
        'guests': Guest.objects.all(),
        'form': form
      }
    )

  data_form = form.cleaned_data

  guest = data_form.get('guest')
  room = data_form.get('room')
  check_in = data_form.get('check_in')
  check_out = data_form.get('check_out')

  Reservation.objects.create(
    guest=guest,
    room=room,
    check_in=check_in,
    check_out=check_out
  )

  messages.success(request, "Reservation added successfully.")
  return redirect('reservations')

def cancel_reservation(request, reservation_id):
  try:
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.delete()

    messages.warning(request, 'Reservation deleted successfully.')
    return redirect('reservations')
  except Reservation.DoesNotExist as error:
    print("ERROR[cancel-reservation]", error)
    messages.error(request, "An error occurred while deleting the reservation.")
    return redirect('reservations')

def add_guest(request):
  if request.method != 'POST':
    messages.error(request, "Method not allowed.")
    return redirect('add-guest')

  form = GuestForm(request.POST)

  if not form.is_valid():
    return render(
      request,
      'forms/guest_form.html',
      {
        'username': 'John Doe',
        'position': 'Manager',
        'title': 'Add Guest',
        'current_path': request.path,
        'form': form
      }
    )

  data_form = form.cleaned_data

  name = data_form.get('name')
  email = data_form.get('email')
  phone = data_form.get('phone')
  preferences = data_form.get('preferences')

  Guest.objects.create(
    name=name,
    email=email,
    phone=phone,
    preference=preferences
  )

  messages.success(request, "Guest added successfully.")
  return redirect('guests')

def delete_guest(request, guest_id):
  try:
    guest = Guest.objects.get(id=guest_id)
    reservations = Reservation.objects.filter(guest__id=guest_id)
    if reservations.exists():
      messages.warning(request, 'Guest has reservations. Please delete them first.')
      return redirect('guests')

    guest.delete()
    messages.warning(request, 'Guest deleted successfully.')
    return redirect('guests')
  except Guest.DoesNotExist as error:
    print("ERROR[delete-guest]", error)
    messages.error(request, "An error occurred while deleting the guest.")
    return redirect('guests')

def update_guest(request, guest_id):
  try:
    guest = Guest.objects.get(id=guest_id)

    form = GuestForm(request.POST)
    if not form.is_valid():
      return render(
        request,
        'forms/guest_form.html',
        {
          'username': 'John Doe',
          'position': 'Manager',
          'title': 'Edit Guest',
          'current_path': request.path,
          'form': form,
          'guest': guest
        }
      )

    data_form = form.cleaned_data

    guest.name = data_form.get('name')
    guest.email = data_form.get('email')
    guest.phone = data_form.get('phone')
    guest.preference = data_form.get('preferences')

    guest.save()
    messages.success(request, 'Guest edited successfully.')
    return redirect('guests')
  except (Guest.DoesNotExist, Exception) as error:
    print("ERROR[delete-guest]", error)
    messages.error(request, "An error occurred while deleting the guest.")
    return redirect('guests')

def add_room(request):
  if request.method != 'POST':
    messages.error(request, "Method not allowed.")
    return redirect('rooms')

  form = RoomForm(request.POST)

  if not form.is_valid():
    return render(
      request,
      'forms/room_form.html',
      {
        'username': 'John Doe',
        'position': 'Manager',
        'title': 'Add Room',
        'current_path': request.path,
        'form': form
      }
    )

  data_form = form.cleaned_data

  number = data_form.get('number')
  room_type = data_form.get('type')
  building = data_form.get('building')
  floor = data_form.get('floor')
  persons = data_form.get('persons')
  beds = data_form.get('beds')

  Room.objects.create(
    number=number,
    type=room_type,
    building=building,
    floor=floor,
    persons=persons,
    beds=beds
  )

  messages.success(request, "Room added successfully.")
  return redirect('rooms')

def update_room(request, room_id):
  room = Room.objects.get(id=room_id)

  form = RoomForm(request.POST)
  if not form.is_valid():
    return render(
      request,
      'forms/room_form.html',
      {
        'username': 'John Doe',
        'position': 'Manager',
        'title': 'Edit Room',
        'current_path': request.path,
        'form': form,
        'room': room
      }
    )

  data_form = form.cleaned_data

  room.number = data_form.get('number')
  room.type = data_form.get('type')
  room.building = data_form.get('building')
  room.floor = data_form.get('floor')
  room.persons = data_form.get('persons')
  room.beds = data_form.get('beds')

  room.save()
  messages.success(request, 'Room edited successfully.')
  return redirect('rooms')



def delete_room(request, room_id):
  try:
    room = Room.objects.get(id=room_id)
    reservations = Reservation.objects.filter(room__id=room_id)
    if reservations.exists():
      messages.warning(request, 'Room has reservations. Please delete them first.')
      return redirect('rooms')

    room.delete()
    messages.warning(request, 'Room deleted successfully.')
    return redirect('rooms')
  except Room.DoesNotExist as error:
    print("ERROR[delete-room]", error)
    messages.error(request, "An error occurred while deleting the room.")
    return redirect('rooms')

def add_building(request):
  if request.method != 'POST':
    messages.error(request, "Method not allowed.")
    return redirect('buildings')

  form = BuildingForm(request.POST)

  if not form.is_valid():
    return render(
      request,
      'forms/building_form.html',
      {
        'username': 'John Doe',
        'position': 'Manager',
        'title': 'Add Building',
        'current_path': request.path,
        'form': form
      }
    )

  data_form = form.cleaned_data

  name = data_form.get('name')
  floors = data_form.get('floors_number')

  Building.objects.create(
    name=name,
    floors_number=floors
  )

  messages.success(request, "Building added successfully.")
  return redirect('buildings')

def update_building(request, building_id):
  building = Building.objects.get(id=building_id)

  form = BuildingForm(request.POST)
  if not form.is_valid():
    return render(
      request,
      'forms/building_form.html',
      {
        'username': 'John Doe',
        'position': 'Manager',
        'title': 'Edit Building',
        'current_path': request.path,
        'form': form,
        'building': building
      }
    )

  data_form = form.cleaned_data

  building.name = data_form.get('name')
  building.floors_number = data_form.get('floors_number')

  building.save()
  messages.success(request, 'Building edited successfully.')
  return redirect('buildings')

def delete_building(request, building_id):
  try:
    if building_id == 0:
      messages.error(request, 'Select a building to delete.')
      return redirect('buildings')

    building = Building.objects.get(id=building_id)
    rooms = Room.objects.filter(building__id=building_id)

    if rooms.exists():
      messages.warning(request, 'Building has rooms. Please delete them first.')
      return redirect('buildings')

    building.delete()
    messages.warning(request, 'Building deleted successfully.')
    return redirect('buildings')
  except Building.DoesNotExist as error:
    print("ERROR[delete-building]", error)
    messages.error(request, "An error occurred while deleting the building.")
    return redirect('buildings')

def add_maintenance(request):
  if request.method != 'POST':
    messages.error(request, "Method not allowed.")
    return redirect('maintenances')

  form = MaintenanceForm(request.POST)

  if not form.is_valid():
    return render(
      request,
      'forms/maintenance_form.html',
      {
        'username': 'John Doe',
        'position': 'Manager',
        'title': 'Add Maintenance',
        'current_path': request.path,
        'form': form
      }
    )

  data_form = form.cleaned_data

  description = data_form.get('description')
  room = data_form.get('room')
  start_date = data_form.get('start_date')
  end_date = data_form.get('end_date')

  Maintenance.objects.create(
    description=description,
    room=room,
    start_date=start_date,
    end_date=end_date
  )

  messages.success(request, "Maintenance added successfully.")
  return redirect('maintenances')

def update_maintenance(request, maintenance_id):
  maintenance = Maintenance.objects.get(id=maintenance_id)

  maintenance.status = 'COMPLETED' if maintenance.status == 'IN_PROGRESS' else 'IN_PROGRESS'

  maintenance.save()

  messages.success(request, 'Maintenance updated successfully.')
  return redirect('maintenances')

def delete_maintenance(request, maintenance_id):
  try:
    maintenance = Maintenance.objects.get(id=maintenance_id)
    maintenance.delete()
    messages.warning(request, 'Maintenance deleted successfully.')
    return redirect('maintenances')
  except Maintenance.DoesNotExist as error:
    print("ERROR[delete-maintenance]", error)
    messages.error(request, "An error occurred while deleting the maintenance.")
    return redirect('maintenances')

urlpatterns = [
    path('save_reservation/', add_reservation, name='save-reservation'),
    path('cancel_reservation/<int:reservation_id>', cancel_reservation, name='cancel-reservation'),
    path('save_guest/', add_guest, name='save-guest'),
    path('update_guest/<int:guest_id>', update_guest, name='update-guest'),
    path('delete_guest/<int:guest_id>', delete_guest, name='delete-guest'),
    path('save_room/', add_room, name='save-room'),
    path('update_room/<int:room_id>', update_room, name='update-room'),
    path('delete_room/<int:room_id>', delete_room, name='delete-room'),
    path('save_building/', add_building, name='save-building'),
    path('update_building/<int:building_id>', update_building, name='update-building'),
    path('delete_building/<int:building_id>', delete_building, name='delete-building'),
    path('save_maintenance/', add_maintenance, name='save-maintenance'),
    path('update_maintenance/<int:maintenance_id>', update_maintenance, name='update-maintenance'),
    path('delete_maintenance/<int:maintenance_id>', delete_maintenance, name='delete-maintenance'),
]
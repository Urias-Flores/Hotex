from datetime import datetime
from django import forms
from django.forms import Form
from django.core.validators import RegexValidator, MaxLengthValidator, MinValueValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import authenticate
from hotex_app.models import Reservation
from hotex_app.models import Guest, Room, Building


def validate_no_past(check_in: datetime):
  if check_in < timezone.now().date():
    raise ValidationError("Check-in date must be in the future.")

class ReservationForm(Form):
  guest = forms.ModelChoiceField(
    queryset=Guest.objects.all(),
    empty_label='-- Select a guest --',
    widget=forms.Select(attrs={
      'class': 'input__field',
      'id': 'guest',
    })
  )

  room = forms.ModelChoiceField(
    queryset=Room.objects.all(),
    empty_label='-- Select a room --',
    widget=forms.Select(attrs={
      'class': 'input__field',
      'id': 'room'
    })
  )

  check_in = forms.DateField(
    widget=forms.DateInput(attrs={
      'type': 'date',
      'class': 'input__field',
      'id': 'check_in_date'
    })
  )

  check_out = forms.DateField(
    widget=forms.DateInput(attrs={
      'type': 'date',
      'class': 'input__field',
      'id': 'check_out_date'
    })
  )

  def clean(self):
    cleaned_data = super().clean()
    check_in: datetime = cleaned_data.get('check_in')
    check_out: datetime = cleaned_data.get('check_out')
    room: Room = cleaned_data.get('room')

    if check_out < check_in:
      raise ValidationError("Check-out date must be after check-in date.")

    if check_in < timezone.now().date():
      raise ValidationError("Check-in date must be in the future.")

    if check_out < timezone.now().date():
      raise ValidationError("Check-out date must be in the future.")

    # verification for availability
    reservations = Reservation.objects.filter(
      room=room,
      check_in__lte=check_out,
      check_out__gte=check_in
    )

    if reservations.exists():
      raise ValidationError("The room is not available for the selected dates.")

    return cleaned_data

class GuestForm(Form):
  id = forms.IntegerField(
    required=False,
    widget=forms.HiddenInput()
  )

  name = forms.CharField(
    validators=[MaxLengthValidator(50, "Name must be at most 50 characters long.")],
    widget=forms.TextInput(attrs={
      'placeholder': 'Type your name...',
      'class': 'input__field',
      'id': 'first_name'
    })
  )

  email = forms.EmailField(
    required=False,
    widget=forms.EmailInput(attrs={
      'placeholder': 'Type your email address, e.g. email@domain.com',
      'type': 'email',
      'class': 'input__field',
      'id': 'email'
    })
  )

  phone = forms.CharField(
    max_length=11,
    validators=[MaxLengthValidator(11, "Phone number must be at most 11 digits long.")],
    widget=forms.TextInput(attrs={
      'placeholder': 'Type your phone number...',
      'class': 'input__field',
      'id': 'phone'
    })
  )

  preferences = forms.CharField(
    required=False,
    validators=[MaxLengthValidator(50, "Preferences must be at most 20 characters long.")],
    widget=forms.Textarea(attrs={
      'placeholder': 'Type your preferences, e.g. smoking, pets, etc.',
      'class': 'input__field input__field--textarea',
      'id': 'preference'
    })
  )

  def clean(self):
    cleaned_data = super().clean()
    guest_id = cleaned_data.get('id')
    email = cleaned_data.get('email')
    phone = cleaned_data.get('phone')

    if email and Guest.objects.exclude(id=guest_id).filter(email=email).exists():
      raise ValidationError("Guest with this email already exists.")

    if phone and Guest.objects.exclude(id=guest_id).filter(phone=phone).exists():
      raise ValidationError("Guest with this phone number already exists.")

    return cleaned_data

class RoomForm(Form):
  id = forms.IntegerField(
    required=False,
    widget=forms.HiddenInput()
  )

  number = forms.CharField(
    widget=forms.TextInput(attrs={
      'type': 'number',
      'placeholder': 'Type the room number...',
      'class': 'input__field',
      'id': 'room_number'
    })
  )

  type = forms.ChoiceField(
    choices=[
      ('SINGLE', 'Single'),
      ('DOUBLE', 'Double'),
      ('SUITE', 'Suite'),
    ],
    widget=forms.Select(attrs={
      'class': 'input__field',
      'id': 'room_type'
    })
  )

  building = forms.ModelChoiceField(
    queryset=Building.objects.all(),
    empty_label='-- Select a building --',
    widget=forms.Select(attrs={
      'class': 'input__field',
      'id': 'building'
    })
  )

  floor = forms.IntegerField(
    min_value=1,
    validators=[MinValueValidator(1, "Floor number must be at least 1.")],
    widget=forms.NumberInput(attrs={
      'type': 'number',
      'placeholder': 'Type the floor number...',
      'class': 'input__field',
      'id': 'floor'
    })
  )

  beds = forms.IntegerField(
    widget=forms.NumberInput(attrs={
      'type': 'number',
      'placeholder': 'Type the number of beds...',
      'class': 'input__field',
      'id': 'beds'
    })
  )

  persons = forms.IntegerField(
    widget=forms.NumberInput(attrs={
      'type': 'number',
      'placeholder': 'Type the number of persons...',
      'class': 'input__field',
      'id': 'persons'
    })
  )

  def clean(self):
    cleaned_data = super().clean()
    room_id = cleaned_data.get('id')
    building = cleaned_data.get('building')
    number = cleaned_data.get('number')
    floor = cleaned_data.get('floor')

    if floor < 1:
      raise ValidationError("Floor number must be at least 1.")

    if Room.objects.exclude(id=room_id).filter(number=number).exists():
      raise ValidationError("Room with this number already exists.")

    building = Building.objects.get(id=building.id)
    if floor > building.floors_number:
      raise ValidationError("Building does not have enough floors.")

    return cleaned_data

class BuildingForm(Form):
  name = forms.CharField(
    validators=[
      MaxLengthValidator(15, "Building name must be at most 20 characters long."),
      RegexValidator(
        regex='^[a-zA-Z0-9 ]+$',
        message='Building name must contain only letters, numbers and spaces.'
      )
    ],
    widget=forms.TextInput(attrs={
      'placeholder': 'Type the building name e. g. Building 1...',
      'class': 'input__field',
      'id': 'building_name'
    })
  )

  floors_number = forms.IntegerField(
    min_value=1,
    validators=[MinValueValidator(1, "Number of floors must be at least 1.")],
    widget=forms.NumberInput(attrs={
      'type': 'number',
      'placeholder': 'Type the number of floors...',
      'class': 'input__field',
      'id': 'floors_number'
    })
  )

class MaintenanceForm(Form):
  description = forms.CharField(
    validators=[
      MaxLengthValidator(50, "Maintenance description must be at most 50 characters long.")
    ],
    widget=forms.Textarea(attrs={
      'placeholder': 'Type the maintenance description...',
      'class': 'input__field input__field--textarea',
      'id': 'description'
    })
  )

  room = forms.ModelChoiceField(
    queryset=Room.objects.all(),
    empty_label='-- Select a room --',
    widget=forms.Select(attrs={
      'class': 'input__field',
      'id': 'room'
    })
  )

  start_date = forms.DateField(
    widget=forms.DateInput(attrs={
      'type': 'date',
      'class': 'input__field',
      'id': 'start_date'
    })
  )

  end_date = forms.DateField(
    widget=forms.DateInput(attrs={
      'type': 'date',
      'class': 'input__field',
      'id': 'end_date'
    })
  )

  def clean(self):
    cleaned_data = super().clean()
    room = cleaned_data.get('room')
    start_date = cleaned_data.get('start_date')
    end_date = cleaned_data.get('end_date')

    if end_date < start_date:
      raise ValidationError("End date must be after start date.")

    if start_date < timezone.now().date():
      raise ValidationError("Start date must be in the future.")

    if end_date < timezone.now().date():
      raise ValidationError("End date must be in the future.")

    if Reservation.objects.filter(room=room, check_in__lte=start_date, check_out__gt=end_date).exists():
      raise ValidationError("The room is already reserved for the selected dates.")

    return cleaned_data

class LoginForm(Form):
  username = forms.CharField(
    widget=forms.TextInput(attrs={
      'placeholder': 'Username...',
      'type': 'text',
      'class': 'input__field',
      'id': 'username'
    })
  )

  password = forms.CharField(
    widget=forms.PasswordInput(attrs={
      'placeholder': 'Type your password...',
      'class': 'input__field',
      'id': 'password'
    })
  )
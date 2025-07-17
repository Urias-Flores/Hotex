from django.db import models

# Create your models here.
from django.db import models

room_types = [
  ('SINGLE', 'Single'),
  ('DOUBLE', 'Double'),
  ('SUITE', 'Suite'),
]

class Building(models.Model):
  objects = models.Manager()
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  floors_number = models.IntegerField(default=1)

  def __str__(self):
    return self.name

class Room(models.Model):
  objects = models.Manager()
  id = models.AutoField(primary_key=True)
  number = models.CharField(max_length=100)
  type = models.CharField(max_length=10, choices=room_types)
  building = models.ForeignKey(Building, on_delete=models.CASCADE)
  floor = models.IntegerField(default=1)
  beds = models.IntegerField(default=1)
  persons = models.IntegerField(default=2)

  def __str__(self):
    return f"Room {self.number}, persons {self.persons}, beds {self.beds}"

class Maintenance(models.Model):
  id = models.AutoField(primary_key=True)
  description = models.TextField(null=True)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  start_date = models.DateField()
  end_date = models.DateField()
  status = models.CharField(
    choices=[
      ('PENDING', 'Pending'),
      ('IN_PROGRESS', 'In Progress'),
      ('COMPLETED', 'Completed')
    ],
    default='PENDING'
  )

class Guest(models.Model):
  objects = models.Manager()
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=120)
  email = models.EmailField()
  phone = models.CharField(max_length=11)
  preference = models.TextField()

  def __str__(self):
    return self.name

class Reservation(models.Model):
  id = models.AutoField(primary_key=True)
  guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  check_in = models.DateField()
  check_out = models.DateField()
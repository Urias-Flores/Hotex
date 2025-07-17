from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from hotex_app.forms import GuestForm
from hotex_app.models import Guest
from urllib.parse import unquote

def guests_page(request):
  guests = Guest.objects.all()
  search = unquote(request.GET.get('search', ''))

  if search:
    guests = Guest.objects.filter(name__icontains=search)

  return (render(
    request,
    'guests.html',
    {
      'user': request.user,
      'title': 'Guests',
      'current_path': request.path,
      'guests': guests,
      'query_params': {
        'search': search
      }
    }))

def add_guest_page(request):
  return render(
    request,
    'forms/guest_form.html',
    {
      'user': request.user,
      'title': 'Add Guest',
      'current_path': request.path,
      'form': GuestForm
    })

def edit_guest_page(request, guest_id):
  try:
    guest = Guest.objects.get(id=guest_id)
    form = GuestForm()

    # initialize fields
    form.fields['id'].initial = guest.id
    form.fields['name'].initial = guest.name
    form.fields['email'].initial = guest.email
    form.fields['phone'].initial = guest.phone
    form.fields['preferences'].initial = guest.preference

    return render(
      request,
      'forms/guest_form.html',
      {
        'user': request.user,
        'title': 'Edit Guest',
        'current_path': request.path,
        'form': form,
        'guest': guest
    })
  except Guest.DoesNotExist as error:
    print("ERROR[edit-guest]", error)
    messages.error(request, "Guest not found.")
    return redirect('guests')

urlpatterns = [
    path('', guests_page, name='guests'),
    path('new/', add_guest_page, name='add-guest'),
    path('edit/<int:guest_id>', edit_guest_page, name='edit-guest'),
]
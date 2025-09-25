from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Event, Guest, Host
from .forms import CSVUploadForm, GuestForm
from .serializers import GuestSerializer


# Create your views here.
@csrf_protect
def username_logic(request, event_name_id):
    event = get_object_or_404(Event, event_name_id=event_name_id)
    if request.method == 'POST':
        username = request.POST.get("username")
        if check_host(username, event):
            return redirect('event_detail', event_name_id=event_name_id)
        else:
            error_message='El usuario es incorrecto'
            return render(request, 'host/username_login.html', {'event': event, 'error': error_message})
    return render(request, 'host/username_login.html', {'event': event})

def event_detail(request, event_name_id):
    event = get_object_or_404(Event, event_name_id=event_name_id)
    guests = Guest.objects.filter(event=event)
    confirmed_guests = guests.filter(assists=True).count()
    return render(request, 'host/event_detail.html', {'event': event, 'guests': guests, 'confirmed': confirmed_guests})

def check_host(username, event):
    host = Host.objects.get(evento=event)
    if host.username == username:
        return True
    else:
        return False

def delete_guest(request, event_name_id, guest_id):
    guest = get_object_or_404(Guest, id=guest_id, event_name_id=event_name_id)
    guest.delete()
    return redirect('event_detail', event_name_id=event_name_id)

@csrf_protect
def edit_guest(request, event_name_id, guest_id):
    event = get_object_or_404(Event, event_name_id=event_name_id)
    guest = get_object_or_404(Guest, id=guest_id, event_id=event.id)
    if request.method == 'POST':
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_name_id=event_name_id)
    else:
        form = GuestForm(instance=guest)

    return render(request, 'host/edit_guest.html', {'form': form, 'event': event,'guest': guest})

@csrf_protect
def add_guest(request, event_name_id):
    event = get_object_or_404(Event, event_name_id=event_name_id)
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.event = event
            guest.save()
            return redirect('event_detail', event_name_id=event_name_id)
    else:
        form = GuestForm()

    return render(request, 'host/add_guest.html', {'form': form, 'event': event})

# Event view
def event_guests_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guests = Guest.objects.filter(event = event)
    form = CSVUploadForm(request.POST, request.FILES)

    return render(request, 'event_guests.html', {'event': event, 'guests': guests, 'form': form})

#Controller - view
@api_view(['GET'])
def get_guest_by_event(request, event_name_id):
    event_name = request.query_params.get('eventName')
    guest_name = request.query_params.get('guestName')

    if not event_name or not guest_name:
        return Response({'error:' 'eventName and guestName are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        event = Event.objects.get(event_name_id=event_name)
    except Event.DoesNotExist:
        return Response({'error:' 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        guest = Guest.objects.get(event=event, name=guest_name)
        serializer = GuestSerializer(guest)
        response_data = serializer.data
        response_data['response'] = 'ok'
    except Guest.DoesNotExist:
        response_data = {
            'name': '',
            'invitations': '',
            'extraGuests':'',
            'assists':'',
            'response': '404',
            'message': 'El invitado no se encuentra o está mal escrito el nombre'
        }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_guest(request, event_name_id):
    event_name = request.query_params.get('eventName')
    guest_name = request.query_params.get('guestName')

    if not event_name or not guest_name:
        return Response({'error:' 'eventName and guestName are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        event = Event.objects.get(event_name_id=event_name)
    except Event.DoesNotExist:
        return Response({'error:' 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        guest = Guest.objects.get(event=event, name=guest_name)
        serializer = GuestSerializer(guest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        response_data = serializer.data
        response_data['response'] = '202'

    except Guest.DoesNotExist:
        response_data = {
            'message': 'guest not updated',
            'response': '200'
        }

    return Response(response_data, status=status.HTTP_200_OK)
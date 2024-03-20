from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import UserForm,Event
from .models import UserForm, Event, Profile, Notification, Invitation
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Add the following import for the login_required decorator
from django.contrib.auth.decorators import login_required
# Add the following import for the Classbased view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import InvitationForm
from django.contrib.auth.models import User
from django.contrib import messages
import googlemaps
import os



# Create your views here.
def home(request):
     events = Event.objects.all()
     return render(request, 'home.html', {'events': events})

@login_required
def notificiations(request, event_id):
   notifications = Notification.objects.filter(recipient=request.user)
   notifications.update(read=True)
   return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user)
    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    events = user.attending_events.all()
    friends = profile.friends.all()
    context = {'profile': profile, 'events': events, 'friends': friends, 'user': user}
    return render(request, 'profile.html', context)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def profile(request):
    return render(request, 'profile.html')

class EventCreate(CreateView):
  model = Event
  fields = ['name', 'date', 'time', 'location', 'description', 'cost']
  success_url = '/'

  def form_valid(self, form):
    form.instance.organizer = self.request.user
    return super().form_valid(form)
  
def events_detail(request, event_id):
   event = Event.objects.get(id=event_id)
   return render(request, 'events/detail.html', {
      'event': event,
   })

def attend_event(request, event_id):
   event = get_object_or_404(Event, pk=event_id)
   event.attendees.add(request.user)
   return redirect('events_detail', event_id=event_id)

def cancel_attend_event(request, event_id):
   event = get_object_or_404(Event, pk=event_id)
   event.attendees.remove(request.user)
   return redirect('events_detail', event_id=event_id)


def invite_friends(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitee_usernames = form.cleaned_data['invitee'].split(',')
            message = form.cleaned_data['message']
            invited_users = []

            for username in invitee_usernames:
                try:
                    user = User.objects.get(username=username.strip())
                    Invitation.objects.create(event=event, inviter=request.user, invitee=user, message=message)
                    invited_users.append(user)
                except User.DoesNotExist:
                    messages.warning(request, f"User with username '{username}' does not exist.")

            if invited_users:
                # Send notification to inviter
                Notification.objects.create(recipient=request.user, message="Invitation sent successfully.")
                
                messages.success(request, "Invitations sent successfully.")
                return redirect('event_detail', event_id=event_id)

    else:
        form = InvitationForm()

    return render(request, 'invite_friends.html', {'event': event, 'form': form})


def update_location(request):
   if request.user.is_authenticated:
      if 'lat' in request.GET and 'lng' in request.GET:
         lat = request.GET['lat']
         lng = request.get['lng']
         request.user.profile.latitude = lat
         request.user.profile.longitude = lng
         request.user.profile.save()
   return render(request, '/')



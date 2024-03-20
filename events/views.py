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
from django.urls import reverse


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


def send_invitation(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    invitation = Invitation(event=event, inviter=request.user)
    invitation.save()

    invitation_url = request.build_absolute_uri(reverse('join_event', kwargs={'invitation_id': invitation.id}))
    
    # You can send the invitation URL to the invitee via email, message, or any other means
    
    messages.success(request, "Invitation sent successfully.")
    return redirect('event_detail', event_id=event_id)

def join_event(request, invitation_id):
    invitation = get_object_or_404(Invitation, pk=invitation_id)

    # Logic to join the event goes here

    return redirect('event_detail', event_id=invitation.event.id)


def invite_friends(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.event = event
            invitation.inviter = request.user
            invitation.save()

            messages.success(request, "Invitations sent successfully.")
            return redirect('events_detail', event_id=event_id)
        else:
            messages.error(request, "Failed to send invitations. Please correct the errors in the form.")
    else:
        form = InvitationForm()

    # Generate the shareable link
    shareable_link = request.build_absolute_uri(reverse('join_event', kwargs={'invitation_id': 'placeholder'}))

    return render(request, 'invite_friends.html', {'event': event, 'form': form, 'shareable_link': shareable_link})
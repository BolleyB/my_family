from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from django.http import JsonResponse

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
def notifications(request):
   notifications = Notification.objects.filter(recipient=request.user)
   print('notifications', notifications)
   notifications.update(read=True)
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


@login_required
def read_notifications(request):
    read_notifications = Notification.objects.filter(recipient=request.user, read=True)
    return render(request, 'read_notifications.html', {'notifications': read_notifications})

@login_required
def unread_notifications(request):
    unread_notifications = Notification.objects.filter(recipient=request.user, read=False)
    return render(request, 'unread_notifications.html', {'notifications': unread_notifications})


def notification_list(request):
   notifications = Notification.objects.filter(recipient=request.user)
   return render(request, 'notifications/notifications_list', {'notification': notifications})


def search_users(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            users = User.objects.filter(username__icontains=query)
            users_data = [{'id': user.id, 'username': user.username} for user in users]
            return JsonResponse(users_data, safe=False)
    return JsonResponse([], safe=False)


def join_event(request, invitation_id):
    invitation = get_object_or_404(Invitation, pk=invitation_id)

    if request.method == 'POST':
        # Process the form submission
        message = request.POST.get('message', '')
        # Add the user to the list of attendees
        invitation.event.attendees.add(request.user)
        # Save the message (if provided)
        if message:
            # Here you can save the message along with the attendance confirmation
            # For example, you might create a model to store the user's message along with the event and user information
            # For simplicity, let's just print the message to the console for now
            print(f"Message from {request.user.username}: {message}")
        # Inform the user that they have successfully joined the event
        messages.success(request, "You have successfully joined the event.")
        return redirect('events_detail', event_id=invitation.event.id)
    
    # Render the join event page with the invitation details
    return render(request, 'join_event.html', {'invitation': invitation})



def send_invitation(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.event = event
            invitation.inviter = request.user
            invitation.save()

            # Create and save notification
            Notification.objects.create(
                sender=request.user,
                recipient=invitation.invitee,
                message=f"You have received an invitation from {request.user.username} for event '{event.name}'."
            )

            # Display a success message
            messages.success(request, "Invitation sent successfully.")
            return redirect('event_detail', event_id=event_id)
        else:
            # Display an error message if form is not valid
            messages.error(request, "Failed to send invitation. Please correct the errors in the form.")
    else:
        form = InvitationForm()

    return render(request, 'invite_friends.html', {'event': event, 'form': form})
from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import UserForm, Event, Profile, Notification, Invitation, Attendance
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
from .forms import ProfileUpdateForm




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
def profile(request, user_id):
    current_user = request.user
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user_id)
    attended_events = Event.objects.filter(attendance__attendee_id=user_id)
    friends = user.profile.get_friends()
    print(friends)
    context = {'profile': profile, 'events': attended_events, 'friends': friends, 'profileuser': user, 'currentuser': current_user}
    return render(request, 'profile.html', context)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = form.save()
      profile = Profile(user=user)
      profile.save()
      user.profile = profile
      user.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)




class EventCreate(LoginRequiredMixin,CreateView):
  model = Event
  fields = ['name', 'date', 'time', 'location', 'description', 'cost']
  success_url = '/'

  def form_valid(self, form):
    form.instance.organizer = self.request.user
    return super().form_valid(form)


@login_required 
def events_detail(request, event_id):
   event = Event.objects.get(id=event_id)
   return render(request, 'events/detail.html', {
      'event': event,
   })

@login_required
def attend_event(request, event_id):
   event = get_object_or_404(Event, pk=event_id)
   event.attendees.add(request.user)
   return redirect('events_detail', event_id=event_id)

@login_required
def cancel_attend_event(request, event_id):
   event = get_object_or_404(Event, pk=event_id)
   event.attendees.remove(request.user)
   return redirect('events_detail', event_id=event_id)

def search_view(request):
    query = request.GET.get('search')  # Get the search query from the request
    query2 = request.GET.get('typeofSearch')  # Get the search type from the request
    print(query2)
    if query:
        # Perform a case-insensitive search using '__icontains'
        results = Event.objects.filter(name__icontains=query)
        if query2 == 'person':
           results = User.objects.filter(username__icontains=query)
    else:
        results = Event.objects.none()  # Return an empty queryset if no query provided
    return render(request, 'search_results.html', {'query': query, 'results': results, 'query2': query2})


@login_required
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

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            request.user.email = profile_form.cleaned_data['user'].email
            request.user.first_name = profile_form.cleaned_data['user'].first_name
            request.user.last_name = profile_form.cleaned_data['user'].last_name
            request.user.save()
            return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'profile_form': profile_form})

@login_required
def add_friend(request, friend_id):
    friend = get_object_or_404(User, pk=friend_id)
    request.user.profile.add_friend(friend.profile)
    return redirect(reverse('profile', kwargs={'user_id': friend_id}))

@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(User, pk=friend_id)
    request.user.profile.remove_friend(friend.profile)
    return redirect(reverse('profile', kwargs={'user_id': friend_id}))
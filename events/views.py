from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect


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

from django.urls import reverse


# Create your views here.
def home(request):
     events = Event.objects.all()
     return render(request, 'home.html', {'events': events})

def notifications(request):
    # Get notifications for the logged-in user
    notifications = Notification.objects.filter(recipient=request.user)

    # Get invitations for the logged-in user
    invitations = Invitation.objects.filter(invitee=request.user)

    return render(request, 'notifications.html', {'notifications': notifications, 'invitations': invitations})


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
    event = Event.objects.get(id =event_id)
    inviter = User.objects.get(id=request.user.id)
    invitees = User.objects.all()
    if request.method == 'POST':
       form = InvitationForm(request.POST, initial={'event': event, 'inviter': inviter })
       if form.is_valid():
          invitation = form.save()
          return redirect('event_detail')
    else:
       form = InvitationForm()
    return render(request, 'send_invitation.html', {'form': form, 'invitees': invitees })
    # event = get_object_or_404(Event, pk=event_id)

    # if request.method == 'POST':
    #     # Process the form data
    #     selected_user_ids = request.POST.getlist('selected_users')

    #     # Send invitations to selected users
    #     for user_id in selected_user_ids:
    #         invitee = User.objects.filter(pk=user_id).first()
    #         print(invitee)
    #         if invitee:
    #             form = InvitationForm(request.POST, event=event, inviter=request.user, invitee=invitee)
    #             invitation = form.save()
    #             print(invitation)
    #             # Send notification to invitee
    #             notification = Notification(
    #                 recipient=invitee,
    #                 event=event,
    #                 message=f"You have received an invitation from {request.user.username} to attend {event.name}."
    #             )
    #             notification.save()

    #     messages.success(request, "Invitations sent successfully.")
    #     return JsonResponse({'message': 'Invitations sent successfully.'})

    # Handle GET request (if needed)
    return JsonResponse({'error': 'GET request not allowed.'}, status=405)
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
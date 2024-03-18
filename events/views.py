from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Event
# Create your views here.
def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

class EventCreate(CreateView):
  model = Event
  fields = ['name', 'date', 'time', 'location', 'description', 'cost', 'organizer', 'attendees']
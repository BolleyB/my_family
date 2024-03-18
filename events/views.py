from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import UserForm, Event
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Add the following import for the login_required decorator
from django.contrib.auth.decorators import login_required
# Add the following import for the Classbased view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
# Create your views here.
def home(request):
    return render(request, 'home.html')
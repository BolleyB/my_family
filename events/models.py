from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(User, related_name='attending_events', through='Attendance')

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.BooleanField(default=False)

class UserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text="Your password must contain at least 8 characters.")
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
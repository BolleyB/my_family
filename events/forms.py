from django import forms
from django.contrib.auth.models import User
from .models import Event, Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['invitee', 'message']

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'))

    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'location', 'description', 'cost']
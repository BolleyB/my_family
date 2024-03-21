from django import forms
from django.contrib.auth.models import User
from .models import Event


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['profile_image']

class InvitationForm(forms.Form):
    invitee = forms.ModelChoiceField(queryset=User.objects.all(), label='Invitee')
    message = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 3}))


class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'))

    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'location', 'description', 'cost']
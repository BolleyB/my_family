from django import forms
from django.contrib.auth.models import User
<<<<<<< HEAD
from .models import Invitation
from .models import Event
=======
from .models import Event, Invitation, Profile
>>>>>>> main


<<<<<<< HEAD
class InvitationForm(forms.Form):
    invitee = forms.ModelChoiceField(queryset=User.objects.all(), label='Invitee')
    message = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 3}))

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'location', 'description', 'cost']
=======
class InvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InvitationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['invitee'].queryset = user.profile.friends.all()

    class Meta:
        model = Invitation
        fields = ['invitee', 'message']




class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'))

    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'location', 'description', 'cost']


class ProfileUpdateForm(forms.ModelForm):
    # Additional fields for the User model
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'user']  # Fields from the Profile model
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # Populate form fields with data from the User model
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        # Save data to both User and Profile models
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return super(ProfileUpdateForm, self).save(commit=commit)
>>>>>>> main

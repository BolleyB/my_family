from django import forms
from django.contrib.auth.models import User
from .models import Profile,Invitation

class InvitationForm(forms.Form):
    invitee = forms.ModelChoiceField(queryset=User.objects.all(), label='Invitee')
    message = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 3}))


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
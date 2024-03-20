from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']
        
class SearchForm(forms.Form):
    query = forms.CharField(label='Search')
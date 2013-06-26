from django import forms

from users.models import Profile

class ProfileForm(forms.ModelForm):
    about = forms.CharField(label='About',
        widget=forms.Textarea(attrs={ 
            'placeholder': 'Tell us a little about you' }))

    class Meta:
        fields = ('about',)
        model  = Profile
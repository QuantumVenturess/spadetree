from django import forms

from users.models import Profile

class ProfileForm(forms.ModelForm):
    about = forms.CharField(label='About',
        widget=forms.Textarea(attrs={ 
            'placeholder': 'Tell us a little about you' }))
    phone = forms.CharField(label='Phone',
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 'maxlength': 10,
            'placeholder': '4081234567' }))

    class Meta:
        fields = ('about', 'phone',)
        model  = Profile
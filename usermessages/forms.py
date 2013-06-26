from django import forms

from usermessages.models import UserMessage

class ReplyMessageForm(forms.ModelForm):
    content = forms.CharField(label='Message', widget=forms.Textarea(
        attrs={
            'autocomplete': 'off',
            'placeholder': 'Type your message here',
        }))

    class Meta:
        fields = ('content',)
        model  = UserMessage
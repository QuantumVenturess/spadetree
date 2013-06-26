from django import forms

from states.models import State

class StateForm(forms.ModelForm):
    name = forms.CharField(label='State',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off', 'placeholder': 'State' }))

    class Meta:
        fields = ('name',)
        model  = State

    def add_prefix(self, field_name):
        field_name_mapping = {
            'name': 'state_name',
        }
        # Look up field name; return original if not found
        field_name = field_name_mapping.get(field_name, field_name)
        return super(StateForm, self).add_prefix(field_name)
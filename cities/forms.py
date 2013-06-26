from django import forms

from cities.models import City

class CityForm(forms.ModelForm):
    name = forms.CharField(label='City',
        widget=forms.TextInput(attrs={ 
            'autocomplete': 'off', 'placeholder' : 'City' }))

    class Meta:
        fields = ('name',)
        model  = City

    def add_prefix(self, field_name):
        field_name_mapping = {
            'name': 'city_name',
        }
        # Look up field name; return original if not found
        field_name = field_name_mapping.get(field_name, field_name)
        return super(CityForm, self).add_prefix(field_name)
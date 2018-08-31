from .models import Animal, Owner, Appointment, Species, Subspecies
from django import forms
from django.utils.translation import ugettext as _


class AnimalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['owner'].initial =1

        self.fields['owner'].widget.attrs['class'] = "autocomplete"
        self.fields['owner'].widget.attrs['autocomplete'] = "off"

        self.fields['name'].widget.attrs['class'] = "autocomplete"
        self.fields['name'].widget.attrs['autocomplete'] = "off"

        self.fields['birth'].widget.attrs['class'] = "datepicker"
        self.fields['birth'].widget.attrs['autocomplete'] = "off"

        self.fields['species'].widget.attrs['class'] = "autocomplete"
        self.fields['species'].widget.attrs['autocomplete'] = "off"

        self.fields['subspecies'].widget.attrs['class'] = "autocomplete"
        self.fields['subspecies'].widget.attrs['autocomplete'] = "off"

    owner = forms.CharField(label=_('Владелец'), max_length=50)
    species = forms.CharField(label=_('Вид'), max_length=40)
    subspecies = forms.CharField(label=_('Порода'), max_length=40)

    class Meta:
        model = Animal
        fields = '__all__'

    def clean_owner(self):
        data_str = self.cleaned_data['owner']
        try:
            data_obj = Owner.objects.get(fio=data_str)
        except Owner.DoesNotExist:
            raise forms.ValidationError(_('Владелец не существует'))
        return data_obj

    def clean_species(self):
        data = self.cleaned_data['species']
        data_obj, c = Species.objects.get_or_create(value=data.capitalize())
        return data_obj

    def clean_subspecies(self):
        data = self.cleaned_data['subspecies']
        data_2 = self.cleaned_data['species']
        obj, c = Subspecies.objects.get_or_create(value=data.capitalize(), species=data_2)
        return obj


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = "__all__"


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['appointment_date'].widget.attrs['class'] = "datepicker"
        self.fields['appointment_date'].widget.attrs['autocomplete'] = "off"

    description = forms.CharField(widget=forms.Textarea())

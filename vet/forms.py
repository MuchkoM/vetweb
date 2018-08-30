from .models import Animal, Owner, Appointment, Species, Subspecies
from django import forms
import logging

logger = logging.getLogger(__name__)


class AnimalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['birth'].widget.attrs['class'] = "datepicker"
        self.fields['birth'].widget.attrs['autocomplete'] = "off"

        self.fields['species_'].widget.attrs['class'] = "autocomplete"
        self.fields['species_'].widget.attrs['autocomplete'] = "off"

        self.fields['subspecies_'].widget.attrs['class'] = "autocomplete"
        self.fields['subspecies_'].widget.attrs['autocomplete'] = "off"

    # owner_ = forms.CharField(label='Владелец', max_length=40)
    species_ = forms.CharField(label='Вид', max_length=40)
    subspecies_ = forms.CharField(label='Порода', max_length=40)

    class Meta:
        model = Animal
        fields = ('owner', 'name', 'birth', 'gender', 'species_', 'subspecies_',
                  'aggressive', 'identification', 'identification_value',
                  'is_sterilization', 'is_die',)

    # def clean_owner_(self):
    #     owner_str = self.cleaned_data['owner_']
    #     try:
    #         owner_obj = Owner.objects.get(fio=owner_str)
    #     except Owner.DoesNotExist:
    #         raise forms.ValidationError('Owner not exist')
    #     owner = owner_obj
    #     return owner_str

    def clean_species_(self):
        data = self.cleaned_data['species_']
        logger.info(data)
        obj, c = Species.objects.get_or_create(value=data)
        return obj.pk

    def clean_subspecies_(self):
        data = self.cleaned_data['subspecies_']
        data_2 = self.cleaned_data['species_']
        obj, c = Subspecies.objects.get_or_create(value=data, species_id=data_2)
        return obj.pk


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

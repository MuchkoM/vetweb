from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from . import models


class OwnerForm(forms.ModelForm):
    class Meta:
        model = models.Owner
        fields = "__all__"


class AnimalForm(forms.ModelForm):
    class Meta:
        model = models.Animal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        obj = kwargs['instance']
        if obj is not None:
            self.initial['owner'] = obj.owner.fio
            self.initial['species'] = obj.species.value
            self.initial['subspecies'] = obj.subspecies.value

        if obj is None:
            try:
                owner = get_object_or_404(models.Owner, pk=self.initial['pk_key'])
                self.initial['owner'] = owner.fio
                self.fields['owner'].disabled = True
            except KeyError:
                pass

        self.fields['owner'].widget.attrs['class'] = "autocomplete"
        self.fields['owner'].widget.attrs['autocomplete'] = "off"

        self.fields['name'].widget.attrs['class'] = "autocomplete"
        self.fields['name'].widget.attrs['autocomplete'] = "off"

        self.fields['date'].widget.attrs['class'] = "datepicker"
        self.fields['date'].widget.attrs['autocomplete'] = "off"

        self.fields['species'].widget.attrs['class'] = "autocomplete"
        self.fields['species'].widget.attrs['autocomplete'] = "off"

        self.fields['subspecies'].widget.attrs['class'] = "autocomplete"
        self.fields['subspecies'].widget.attrs['autocomplete'] = "off"

    owner = forms.CharField(label=_('Владелец'), max_length=50)
    species = forms.CharField(label=_('Вид'), max_length=40)
    subspecies = forms.CharField(label=_('Порода'), max_length=40)

    def clean_owner(self):
        data_str = self.cleaned_data['owner']
        try:
            data_obj = models.Owner.objects.get(fio=data_str)
        except models.Owner.DoesNotExist:
            raise forms.ValidationError(_('Владелец не существует'))
        return data_obj

    def clean_species(self):
        data = self.cleaned_data['species']
        data_obj, c = models.Species.objects.get_or_create(value=data.capitalize())
        return data_obj

    def clean_subspecies(self):
        data = self.cleaned_data['subspecies']
        data_2 = self.cleaned_data['species']
        obj, c = models.Subspecies.objects.get_or_create(value=data.capitalize(), species=data_2)
        return obj


class AnimalProceduresForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        obj = kwargs['instance']
        pk = self.initial.get('pk_key', None)

        if pk:
            animal = get_object_or_404(models.Animal, pk=pk)
            self.initial['animal'] = animal.name

        if obj is not None:
            self.initial['animal'] = obj.animal.name
            self.initial['vaccination'] = obj.vaccination.value
            self.fields['animal'].disabled = True

        self.fields['date'].widget.attrs['class'] = "datepicker"
        self.fields['date'].widget.attrs['autocomplete'] = "off"

        self.fields['animal'].widget.attrs['class'] = "autocomplete"
        self.fields['animal'].widget.attrs['autocomplete'] = "off"

    animal = forms.CharField(label=_('Животное'), max_length=40)

    def clean_animal(self):
        data_str = self.cleaned_data['animal']
        try:
            data_obj = models.Animal.objects.get(name=data_str)
        except models.Animal.DoesNotExist:
            raise forms.ValidationError(_('Животного не существует'))
        return data_obj


class PreventionForm(AnimalProceduresForm):
    class Meta:
        model = models.Prevention
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['vaccination'].widget.attrs['class'] = "autocomplete"
        self.fields['vaccination'].widget.attrs['autocomplete'] = "off"

    vaccination = forms.CharField(label=_('Вакцина'), max_length=40)

    def clean_vaccination(self):
        data = self.cleaned_data['vaccination']
        data_obj, c = models.Vaccination.objects.get_or_create(value=data.capitalize())
        return data_obj

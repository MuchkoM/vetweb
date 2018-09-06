from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from . import models


class AutocompleteCharField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['class'] = "autocomplete"
        self.widget.attrs['autocomplete'] = "off"


class DateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['date'].widget.attrs['class'] = "datepicker"
            self.fields['date'].widget.attrs['autocomplete'] = "off"
        except KeyError:
            pass


class ParamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_update = kwargs['instance']
        self.creator_pk = self.initial.pop('_pk', None)


class TitledForm(forms.ModelForm):
    title_action: str = None
    title_model: str = None
    title_button: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_action = _('Обновление') if kwargs['instance'] is not None else _('Добавление')
        self.title_button = _('Обновить') if kwargs['instance'] is not None else _('Добавить')

    def get_title(self):
        return f'{self.title_action} {self.title_model}'


class OwnerForm(TitledForm):
    title_model = _("владельца")

    class Meta:
        model = models.Owner
        fields = "__all__"


class AnimalForm(ParamForm, TitledForm, DateForm):
    title_model = _('животного')

    class Meta:
        model = models.Animal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.creator_pk is not None:
            owner = get_object_or_404(models.Owner, pk=self.creator_pk)
            self.initial['owner_id'] = owner.pk
            self.initial['owner'] = str(owner)
            self.fields['owner'].disabled = True

        if self.instance_update is not None:
            self.initial['owner'] = self.instance_update.owner.__str__()
            self.initial['owner_pk'] = self.instance_update.owner.pk
            self.initial['species'] = self.instance_update.species.value
            self.initial['subspecies'] = self.instance_update.subspecies.value

    owner = AutocompleteCharField(label=_('Владелец'), max_length=50, strip=False)
    owner_id = forms.IntegerField(widget=forms.HiddenInput())
    species = AutocompleteCharField(label=_('Вид'), max_length=40)
    subspecies = AutocompleteCharField(label=_('Порода'), max_length=40)

    def clean(self):
        cleaned_data = super().clean()

        species_str = self.cleaned_data['species']
        subspecies_str = self.cleaned_data['subspecies']

        species, c = models.Species.objects.get_or_create(value=species_str)
        subspecies, c = models.Subspecies.objects.get_or_create(value=subspecies_str, species=species)

        cleaned_data['species'] = species
        cleaned_data['subspecies'] = subspecies

        owner_id = cleaned_data['owner_id']
        try:
            owner_str = cleaned_data['owner']
            owner = models.Owner.objects.get(pk=owner_id)
            owner_str_2 = str(owner)
            if owner_str_2 != owner_str:
                cleaned_data.pop('owner')
                self.add_error('owner', _('Владелец введён неправильно'))
            cleaned_data['owner'] = owner
        except models.Owner.DoesNotExist:
            self.add_error('owner', _('Владелец введён неправильно'))

        return cleaned_data


class AnimalProceduresForm(ParamForm, TitledForm, DateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['animal'].disabled = True

        if self.creator_pk is not None:
            animal = get_object_or_404(models.Animal, pk=self.creator_pk)
            self.initial['animal'] = animal.name

        if self.instance_update is not None:
            self.initial['animal'] = self.instance_update.animal.name

    animal = AutocompleteCharField(label=_('Животное'), max_length=40)

    def clean_animal(self):
        name_animal = self.cleaned_data['animal']
        try:
            data_obj = models.Animal.objects.filter(name=name_animal).first()
        except models.Animal.DoesNotExist:
            raise forms.ValidationError(_('Животного не существует'))
        return data_obj


class PreventionForm(AnimalProceduresForm):
    title_model = _('вакцинации')

    class Meta:
        model = models.Prevention
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance_update is not None:
            self.initial['vaccination'] = self.instance_update.vaccination.value

    vaccination = AutocompleteCharField(label=_('Вакцина'), max_length=40)

    def clean_vaccination(self):
        vaccination_str = self.cleaned_data['vaccination']
        vaccination, c = models.Vaccination.objects.get_or_create(value=vaccination_str)
        return vaccination


class TherapyForm(AnimalProceduresForm):
    title_model = _('терапии')

    class Meta:
        model = models.Therapy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance_update is not None:
            self.initial['diagnosis'] = self.instance_update.diagnosis.value

    diagnosis = AutocompleteCharField(label=_('Диагноз'), max_length=40)

    def clean_diagnosis(self):
        diagnosis_str = self.cleaned_data['diagnosis']
        diagnosis, c = models.Diagnosis.objects.get_or_create(value=diagnosis_str)
        return diagnosis

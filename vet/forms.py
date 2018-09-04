from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from . import models


# todo Придумать способ разделения владельцев и собак при поиске серез импут

class ParamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exist_obj = kwargs['instance']
        self.creator_pk = self.initial.pop('_pk', None)


class TitledForm(forms.ModelForm):
    title_action: str = None
    title_model: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_action = _('Обновление') if kwargs['instance'] is not None else _('Добавление')

    def get_title(self):
        return f'{self.title_action} {self.title_model}'


class OwnerForm(TitledForm):
    title_model = _("владельца")

    class Meta:
        model = models.Owner
        fields = "__all__"


class AnimalForm(ParamForm, TitledForm):
    title_model = _('животного')

    class Meta:
        model = models.Animal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.creator_pk is not None:
            owner = get_object_or_404(models.Owner, pk=self.creator_pk)
            self.initial['owner'] = owner.fio
            self.fields['owner'].disabled = True

        if self.exist_obj is not None:
            self.initial['owner'] = self.exist_obj.owner.fio
            self.initial['species'] = self.exist_obj.species.value
            self.initial['subspecies'] = self.exist_obj.subspecies.value

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
            if self.creator_pk is not None:
                data_obj = models.Owner.objects.get(pk=self.creator_pk)
            else:
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


class AnimalProceduresForm(ParamForm, TitledForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.creator_pk is not None:
            animal = get_object_or_404(models.Animal, pk=self.creator_pk)
            self.initial['animal'] = animal.name
            self.fields['animal'].disabled = True

        if self.exist_obj is not None:
            self.initial['animal'] = self.exist_obj.animal.name
            self.fields['animal'].disabled = True

        self.fields['date'].widget.attrs['class'] = "datepicker"
        self.fields['date'].widget.attrs['autocomplete'] = "off"

        self.fields['animal'].widget.attrs['class'] = "autocomplete"
        self.fields['animal'].widget.attrs['autocomplete'] = "off"

    animal = forms.CharField(label=_('Животное'), max_length=40)

    def clean_animal(self):
        data_str = self.cleaned_data['animal']
        try:
            # todo Need do normal search  can be bad
            # todo Если имя не уникально, get возвращает более одного объекта
            # todo нужно что-то придумать
            data_obj = models.Animal.objects.get(name=data_str)
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

        if self.exist_obj is not None:
            self.initial['vaccination'] = self.exist_obj.vaccination.value

        self.fields['vaccination'].widget.attrs['class'] = "autocomplete"
        self.fields['vaccination'].widget.attrs['autocomplete'] = "off"

    vaccination = forms.CharField(label=_('Вакцина'), max_length=40)

    def clean_vaccination(self):
        data = self.cleaned_data['vaccination']
        data_obj, c = models.Vaccination.objects.get_or_create(value=data.capitalize())
        return data_obj


class TherapyForm(AnimalProceduresForm):
    title_model = _('терапии')

    class Meta:
        model = models.Therapy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.exist_obj is not None:
            self.initial['diagnosis'] = self.exist_obj.diagnosis.value
        self.fields['diagnosis'].widget.attrs['class'] = "autocomplete"
        self.fields['diagnosis'].widget.attrs['autocomplete'] = "off"

    diagnosis = forms.CharField(label=_('Диагноз'), max_length=40)

    def clean_diagnosis(self):
        data = self.cleaned_data['diagnosis']
        data_obj, c = models.Diagnosis.objects.get_or_create(value=data.capitalize())
        return data_obj

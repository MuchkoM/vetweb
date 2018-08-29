from .models import Animal, Owner, Appointment
from django import forms


class AnimalForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(AnimalForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'autocomplete'
    #species = forms.CharField(widget=forms.TextInput(attrs={'class': 'autocomplete'}))
    #subspecies = forms.CharField(widget=forms.TextInput(attrs={'class': 'autocomplete'}))

    class Meta:
        model = Animal
        fields = "__all__"
        labels = {
            'owner': 'Владелец',
            'name': 'Кличка',
            'birth': 'Дата рождения',
            'gender': 'Пол',
            'species': 'Вид',
            'subspecies': 'Порода',
            'aggressive': 'Агрессивность',
            'identification': 'Индефикация',
            'identification_value': 'Код индефикации',
            'is_sterilization': 'Стериализация',
            'is_die': 'Погибло',
        }


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = "__all__"
        labels = {
            'fio': 'ФИО',
            'address': 'Адресс',
            'phone': 'Телефон',
            'email': 'Эл. Почта',
        }


class AppointmentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {'appointment_date': forms.DateInput(attrs={'class': 'datepicker'})}

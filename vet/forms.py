from .models import Animal, Owner, Appointment
from django import forms


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['birth'].widget.attrs['class'] = "datepicker"
        self.fields['birth'].widget.attrs['autocomplete'] = "off"

        self.fields['species'].widget.attrs['class'] = "autocomplete"
        self.fields['species'].widget.attrs['autocomplete'] = "off"

        self.fields['subspecies'].widget.attrs['class'] = "autocomplete"
        self.fields['subspecies'].widget.attrs['autocomplete'] = "off"

        self.fields['owner'].label = 'Владелец'
        self.fields['name'].label = 'Кличка'
        self.fields['birth'].label = 'Дата рождения'
        self.fields['gender'].label = 'Пол'
        self.fields['species'].label = 'Вид'
        self.fields['subspecies'].label = 'Порода'
        self.fields['aggressive'].label = 'Агрессивность'
        self.fields['identification'].label = 'Идентификация'
        self.fields['identification_value'].label = 'Код идентификация'
        self.fields['is_sterilization'].label = 'Стериализация'
        self.fields['is_die'].label = 'Погибло'

    species = forms.CharField()
    subspecies = forms.CharField()


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

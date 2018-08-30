from .models import Animal, Owner, Appointment
from django import forms


class AnimalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['birth'].widget.attrs['class'] = "datepicker"
        self.fields['birth'].widget.attrs['autocomplete'] = "off"

        self.fields['species'].widget.attrs['class'] = "autocomplete"
        self.fields['species'].widget.attrs['autocomplete'] = "off"

        self.fields['subspecies'].widget.attrs['class'] = "autocomplete"
        self.fields['subspecies'].widget.attrs['autocomplete'] = "off"

        self.fields['species'].label = 'Вид'
        self.fields['subspecies'].label = 'Порода'

   # species = forms.CharField()
   # subspecies = forms.CharField()

    class Meta:
        model = Animal
        fields = "__all__"


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

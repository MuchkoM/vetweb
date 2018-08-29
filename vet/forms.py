from .models import Animal, Owner, Appointment
from django import forms


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = "__all__"


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = "__all__"


class AppointmentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {'appointment_date': forms.DateInput(attrs={'class': 'datepicker'})}

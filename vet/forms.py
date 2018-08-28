from django.contrib.auth.models import User
from .models import Animal, Owner, Appointment
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = "__all__"
        widgets = {'birth': forms.DateInput(attrs={'class': 'datepicker'})}


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

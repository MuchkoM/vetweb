from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    title_button = 'Зарегестрироваться'
    get_title = 'Регистрация'
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()

        if self.is_valid():
            user = self.save(commit=False)
            username = cleaned_data['username']
            password = cleaned_data['password']
            user.set_password(password)
            user.save()

        return cleaned_data

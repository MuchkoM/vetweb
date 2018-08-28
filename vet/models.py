from django.db import models
from django.urls import reverse


class Owner(models.Model):
    fio = models.CharField(max_length=50)
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=14)
    email = models.EmailField(max_length=50, blank=True)

    def get_absolute_url(self):
        return reverse('vet:owner-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.fio


class Animal(models.Model):
    GENDER_CHOICE = (
        ('F', 'Самка'),
        ('M', 'Самец'),
    )
    AGGRESSIVE_CHOICE = (
        ('L', 'Низкая'),
        ('M', 'Средняя'),
        ('H', 'Высокая'),
    )
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    birth = models.DateField(blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    genus = models.CharField(max_length=50)
    spec = models.CharField(max_length=50)
    aggressive = models.CharField(max_length=1, choices=AGGRESSIVE_CHOICE)
    is_live = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('vet:animal-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.genus} {self.name}'


class Appointment(models.Model):
    APPOINTMENT_CHOICE = (
        ('S', 'Cтационар'),
        ('A', 'Амбулатор')
    )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    appointment_date = models.DateField(blank=False)
    type = models.CharField(max_length=1, choices=APPOINTMENT_CHOICE)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.appointment_date}'

from django.db import models
from django.urls import reverse


class Owner(models.Model):
    fio = models.CharField(max_length=50)
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=14, blank=True)
    email = models.EmailField(max_length=50, blank=True)

    def get_absolute_url(self):
        return reverse('vet:owner-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.fio}'


class Species(models.Model):
    value = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.value}'


class Subspecies(models.Model):
    value = models.CharField(max_length=40)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.value}'


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
    IDENTIFICATION_CHOICE = (
        ('_', 'Отсутствует'),
        ('C', 'Чипирование'),
        ('S', 'Клеймо'),
    )

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    birth = models.DateField(blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING)
    subspecies = models.ForeignKey(Subspecies, on_delete=models.DO_NOTHING)
    aggressive = models.CharField(max_length=1, choices=AGGRESSIVE_CHOICE)
    identification = models.CharField(max_length=1, choices=IDENTIFICATION_CHOICE)
    identification_value = models.CharField(max_length=50, blank=True)
    is_sterilization = models.BooleanField(default=False)
    is_live = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('vet:animal-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.species} {self.name}'


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

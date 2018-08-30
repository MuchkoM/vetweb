from django.db import models
from django.urls import reverse


class Owner(models.Model):
    fio = models.CharField(verbose_name='ФИО', max_length=50)
    address = models.CharField(verbose_name='Адрес', max_length=70, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=14, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=50, blank=True)

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
        return f'{self.species} {self.value}'


class Animal(models.Model):
    AGGRESSIVE_LOW = 'l'
    AGGRESSIVE_MEDIUM = 'm'
    AGGRESSIVE_HIGH = 'h'
    AGGRESSIVE_CHOICE = (
        (AGGRESSIVE_LOW, 'Низкая'),
        (AGGRESSIVE_MEDIUM, 'Средняя'),
        (AGGRESSIVE_HIGH, 'Высокая'),
    )

    GENDER_MALE = True
    GENDER_FEMALE = False
    GENDER_CHOICE = (
        (GENDER_MALE, 'Самец'),
        (GENDER_FEMALE, 'Самка'),
    )

    IDENTIFICATION_NONE = 'n'
    IDENTIFICATION_CHIP = 'c'
    IDENTIFICATION_STIGMA = 's'
    IDENTIFICATION_CHOICE = (
        (IDENTIFICATION_NONE, 'Отсутствует'),
        (IDENTIFICATION_CHIP, 'Чипирование'),
        (IDENTIFICATION_STIGMA, 'Клеймо'),
    )

    YES = True
    NO = False
    YES_NO_CHOICE = (
        (YES, 'Да'),
        (NO, 'Нет'),
    )

    owner = models.ForeignKey(Owner, verbose_name='Владелец',
                              on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Кличка',
                            max_length=50)
    birth = models.DateField(verbose_name='Дата рождения',
                             blank=False)
    gender = models.BooleanField(verbose_name='Пол',
                                 choices=GENDER_CHOICE,
                                 default=GENDER_MALE)
    species = models.ForeignKey(Species, verbose_name='Вид',
                                on_delete=models.DO_NOTHING)
    subspecies = models.ForeignKey(Subspecies,
                                   verbose_name='Порода',
                                   on_delete=models.DO_NOTHING,
                                   null=True)
    aggressive = models.CharField(verbose_name='Агрессивность',
                                  max_length=1,
                                  choices=AGGRESSIVE_CHOICE,
                                  default=AGGRESSIVE_LOW)
    identification = models.CharField(verbose_name='Идентификация',
                                      max_length=1,
                                      choices=IDENTIFICATION_CHOICE,
                                      default=IDENTIFICATION_NONE)
    identification_value = models.CharField(verbose_name='Код идентификации',
                                            max_length=50,
                                            blank=True)
    is_sterilization = models.BooleanField(verbose_name='Стериализация',
                                           choices=YES_NO_CHOICE,
                                           default=NO)
    is_die = models.BooleanField(verbose_name='Погибло',
                                 choices=YES_NO_CHOICE,
                                 default=NO)

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

    def get_absolute_url(self):
        return reverse('vet:appointment-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.appointment_date}'

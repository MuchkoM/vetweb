from datetime import date

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _


class OwnerManager(models.Manager):
    def owners_by_term(self, term: str):
        q1 = self.filter(fio__contains=term)
        q2 = self.filter(address__contains=term)
        return (q1 | q2).distinct()


class Owner(models.Model):
    class Meta:
        unique_together = ('fio', 'address',)
        ordering = ("-date",)

    fio = models.CharField(verbose_name=_('ФИО'), max_length=50)
    address = models.CharField(verbose_name=_('Адрес'), max_length=70, blank=True)
    phone = models.CharField(verbose_name=_('Телефон'), max_length=14, blank=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=50, blank=True)
    date = models.DateTimeField(auto_now=True)

    objects = OwnerManager()

    def get_absolute_url(self):
        return reverse('vet:owner-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.fio} {self.address}'


class ValuesModel(models.Model):
    value = models.CharField(max_length=40, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        abstract = True
        ordering = ("-date",)


class Species(ValuesModel):
    pass


class Subspecies(ValuesModel):
    class Meta:
        unique_together = ('value', 'species',)

    value = models.CharField(max_length=40)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.species.value} {self.value}'


class AnimalManager(models.Manager):
    def live_animals(self):
        return self.filter(is_die__exact=False)

    def die_animals(self):
        return self.filter(is_die__exact=True)


class Animal(models.Model):
    AGGRESSIVE_LOW = 'l'
    AGGRESSIVE_MEDIUM = 'm'
    AGGRESSIVE_HIGH = 'h'
    AGGRESSIVE_CHOICE = (
        (AGGRESSIVE_LOW, _('Низкая')),
        (AGGRESSIVE_MEDIUM, _('Средняя')),
        (AGGRESSIVE_HIGH, _('Высокая')),
    )

    GENDER_MALE = True
    GENDER_FEMALE = False
    GENDER_CHOICE = (
        (GENDER_MALE, _('Самец')),
        (GENDER_FEMALE, _('Самка')),
    )

    IDENTIFICATION_NONE = 'n'
    IDENTIFICATION_CHIP = 'c'
    IDENTIFICATION_STIGMA = 's'
    IDENTIFICATION_CHOICE = (
        (IDENTIFICATION_NONE, _('Отсутствует')),
        (IDENTIFICATION_CHIP, _('Чипирование')),
        (IDENTIFICATION_STIGMA, _('Клеймо')),
    )

    YES = True
    NO = False
    YES_NO_CHOICE = (
        (YES, _('Да')),
        (NO, _('Нет')),
    )
    objects = AnimalManager()

    owner = models.ForeignKey(Owner, verbose_name=_('Владелец'),
                              on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Кличка'),
                            max_length=50)
    species = models.ForeignKey(Species, verbose_name=_('Вид'),
                                on_delete=models.DO_NOTHING)
    subspecies = models.ForeignKey(Subspecies,
                                   verbose_name=_('Порода'),
                                   on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name=_('Дата рождения'),
                            blank=False, default=date.today)
    gender = models.BooleanField(verbose_name=_('Пол'),
                                 choices=GENDER_CHOICE,
                                 default=GENDER_MALE)
    aggressive = models.CharField(verbose_name=_('Агрессивность'),
                                  choices=AGGRESSIVE_CHOICE,
                                  default=AGGRESSIVE_LOW,
                                  max_length=1)
    identification = models.CharField(verbose_name=_('Идентификация'),
                                      choices=IDENTIFICATION_CHOICE,
                                      default=IDENTIFICATION_NONE,
                                      max_length=1)
    identification_value = models.CharField(verbose_name=_('Код идентификации'),
                                            max_length=50,
                                            blank=True)
    is_sterilization = models.BooleanField(verbose_name=_('Стериализация'),
                                           choices=YES_NO_CHOICE,
                                           default=NO)
    is_die = models.BooleanField(verbose_name=_('Погибло'),
                                 choices=YES_NO_CHOICE,
                                 default=NO)

    def get_absolute_url(self):
        return reverse('vet:animal-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.species} {self.name}'


class AnimalProcedures(models.Model):
    animal = models.ForeignKey(Animal, verbose_name=_('Животное'), on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_('Дата'), blank=False, default=date.today)
    procedure_type = None

    def __str__(self):
        return f'{self.procedure_type} {self.date}'

    def get_absolute_url(self):
        return reverse('vet:animal-detail', kwargs={'pk': self.animal.pk})

    class Meta:
        abstract = True
        ordering = ("-date",)


class Vaccination(ValuesModel):
    pass


class Diagnosis(ValuesModel):
    pass


class Prevention(AnimalProcedures):
    procedure_type = _('Вакцинация')
    TYPE_FIRST = 'f'
    TYPE_AGAIN = 'a'
    TYPE_REPEAT = 'r'
    TYPE_CHOICE = (
        (TYPE_FIRST, _('Первичная')),
        (TYPE_AGAIN, _('Повторная')),
        (TYPE_REPEAT, _('Ревакцинация')),
    )
    vaccination = models.ForeignKey(Vaccination, verbose_name=_('Прививка'),
                                    on_delete=models.DO_NOTHING)
    type_vaccination = models.CharField(verbose_name=_('Тип прививки'), max_length=1,
                                        choices=TYPE_CHOICE,
                                        default=TYPE_FIRST)

    def get_vaccination(self):
        return self.vaccination.value if self.vaccination is not None else ''


class Therapy(AnimalProcedures):
    procedure_type = _('Терапия')
    THERAPY_CLINIC = 'c'
    THERAPY_OPERATIVE = 'o'
    THERAPY_TYPE = (
        (THERAPY_CLINIC, _('Амбулатория')),
        (THERAPY_OPERATIVE, _('Хирургия')),
    )
    type = models.CharField(verbose_name=_('Тип терапии'), max_length=1,
                            choices=THERAPY_TYPE,
                            default=THERAPY_CLINIC)
    symptomatic = models.CharField(verbose_name=_('Симптомы'), max_length=100, blank=True)
    labs = models.CharField(verbose_name=_('Исследования'), max_length=100, blank=True)
    diagnosis = models.ForeignKey(Diagnosis, verbose_name=_('Диагноз'),
                                  on_delete=models.DO_NOTHING)

    def get_diagnosis(self):
        return self.diagnosis.value if self.diagnosis is not None else ''

import json

from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from . import models


class ParamCreateView(generic.CreateView):
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk', None)
        if pk:
            initial['_pk'] = pk
        return initial


class AjaxRequest:
    @classmethod
    def get_ajax(cls, request):
        if request.is_ajax():
            kwargs = request.GET.dict()
            result = list(cls.get_queryset_value(kwargs))
            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

    @staticmethod
    def get_queryset_value(kwarg: dict) -> QuerySet:
        pass


class OwnerView:
    class Create(generic.CreateView):
        form_class = forms.OwnerForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(generic.DetailView):
        model = models.Owner
        template_name = 'vet/owner/detail.html'

    class List(generic.ListView):
        model = models.Owner
        template_name = 'vet/owner/list.html'

    class Update(generic.UpdateView):
        form_class = forms.OwnerForm
        model = models.Owner
        template_name = 'vet/generic/generic_form.html'

    class Delete(generic.DeleteView):
        model = models.Owner
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:owner-list')


class AnimalView:
    class Create(ParamCreateView):
        form_class = forms.AnimalForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(generic.DetailView):
        model = models.Animal
        template_name = 'vet/animal/detail.html'

    class List(generic.ListView):
        model = models.Animal
        template_name = 'vet/animal/list.html'

    class Update(generic.UpdateView):
        form_class = forms.AnimalForm
        model = models.Animal
        template_name = 'vet/generic/generic_form.html'

    class Delete(generic.DeleteView):
        model = models.Animal
        template_name = 'vet/generic/generic_confirm_delete.html'

        def get_success_url(self):
            owner_pk = self.object.owner.pk
            return reverse_lazy('vet:owner-detail', kwargs={'pk': owner_pk})


class PreventionView:
    class Create(ParamCreateView):
        form_class = forms.PreventionForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(generic.DetailView):
        model = models.Prevention
        template_name = 'vet/prevention/detail.html'

    class List(generic.ListView):
        model = models.Prevention
        template_name = 'vet/prevention/list.html'

    class Update(generic.UpdateView):
        form_class = forms.PreventionForm
        model = models.Prevention
        template_name = 'vet/generic/generic_form.html'

    class Delete(generic.DeleteView):
        model = models.Prevention
        template_name = 'vet/generic/generic_confirm_delete.html'

        def get_success_url(self):
            animal_pk = self.object.animal.pk
            return reverse_lazy('vet:animal-detail', kwargs={'pk': animal_pk})


class TherapyView:
    class Create(ParamCreateView):
        form_class = forms.TherapyForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(generic.DetailView):
        model = models.Therapy
        template_name = 'vet/therapy/detail.html'

    class List(generic.ListView):
        model = models.Therapy
        template_name = 'vet/therapy/list.html'

    class Update(generic.UpdateView):
        form_class = forms.TherapyForm
        model = models.Therapy
        template_name = 'vet/generic/generic_form.html'

    class Delete(generic.DeleteView):
        model = models.Therapy
        template_name = 'vet/generic/generic_confirm_delete.html'

        def get_success_url(self):
            animal_pk = self.object.animal.pk
            return reverse_lazy('vet:animal-detail', kwargs={'pk': animal_pk})


class Ajax:
    class Owner(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Owner.objects.filter(
                fio__contains=kwarg['term'])[:10].values_list('fio', flat=True)

    class Animal(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Animal.objects.filter(
                name__icontains=kwarg['term'])[:10].values_list('name', flat=True)

    class Species(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Species.objects.filter(
                value__icontains=kwarg['term'])[:10].values_list('value', flat=True)

    class Subspecies(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Subspecies.objects.filter(species__value=kwarg['term_2']).filter(
                value__icontains=kwarg['term'])[:10].values_list('value', flat=True)

    class Vaccination(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Vaccination.objects.filter(
                value__icontains=kwarg['term'])[:10].values_list('value', flat=True)

    class Diagnosis(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Diagnosis.objects.filter(
                value__icontains=kwarg['term'])[:10].values_list('value', flat=True)

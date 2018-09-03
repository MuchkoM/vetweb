from django.db.models import QuerySet
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from . import models
from . import forms
import json


class CreateViewPk(generic.CreateView):
    def get_initial(self):
        initial = super().get_initial()
        initial['_pk'] = self.kwargs.get('pk', None)
        return initial


class AjaxRequest:
    @classmethod
    def get_ajax(cls, request):
        if request.is_ajax():
            result = list(cls.get_queryset_value(request.GET.dict()))
            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

    @staticmethod
    def get_queryset_value(args) -> QuerySet:
        pass


class OwnerView:
    class Create(generic.CreateView):
        form_class = forms.OwnerForm
        template_name = 'vet/owner/form.html'

    class Detail(generic.DetailView):
        model = models.Owner
        template_name = 'vet/owner/detail.html'

    class List(generic.ListView):
        model = models.Owner
        template_name = 'vet/owner/list.html'

    class Update(generic.UpdateView):
        form_class = forms.OwnerForm
        model = models.Owner
        template_name = 'vet/owner/form.html'

    class Delete(generic.DeleteView):
        model = models.Owner
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:owner-list')


class AnimalView:
    class Create(CreateViewPk):
        form_class = forms.AnimalForm
        template_name = 'vet/animal/form.html'

    class Detail(generic.DetailView):
        model = models.Animal
        template_name = 'vet/animal/detail.html'

    class List(generic.ListView):
        model = models.Animal
        template_name = 'vet/animal/list.html'

    class Update(generic.UpdateView):
        form_class = forms.AnimalForm
        model = models.Animal
        template_name = 'vet/animal/form.html'

    class Delete(generic.DeleteView):
        model = models.Animal
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:animal-list')


class PreventionView:
    class Create(CreateViewPk):
        form_class = forms.PreventionForm
        template_name = 'vet/prevention/form.html'

    class Detail(generic.DetailView):
        model = models.Prevention
        template_name = 'vet/prevention/detail.html'

    class List(generic.ListView):
        model = models.Prevention
        template_name = 'vet/prevention/list.html'

    class Update(generic.UpdateView):
        form_class = forms.PreventionForm
        model = models.Prevention
        template_name = 'vet/prevention/form.html'

    class Delete(generic.DeleteView):
        model = models.Prevention
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:prevention-list')


class Ajax:
    class Species(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Species.objects.filter(value__icontains=kwarg['term'])[:10].values_list('value', flat=True)

    class Subspecies(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Subspecies.objects.filter(species__value=kwarg['term_2']).filter(
                value__icontains=kwarg['term'])[:10].values_list('value', flat=True)

    class Owner(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Owner.objects.filter(fio__icontains=kwarg['term'])[:10].values_list('fio', flat=True)

    class Animal(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Animal.objects.filter(name__icontains=kwarg['term'])[:10].values_list('name', flat=True)

    class Vaccination(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            return models.Vaccination.objects.filter(value__icontains=kwarg['term'])[:10].values_list('value',
                                                                                                      flat=True)

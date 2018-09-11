import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from . import models


class AuthRequireView(LoginRequiredMixin):
    pass


class SearchView(AuthRequireView, generic.TemplateView):
    template_name = 'vet/search.html'

    def get_context_data(self):
        q = self.request.GET['q']
        owners_fio = models.Owner.objects.filter(fio__contains=q)
        owners_address = models.Owner.objects.filter(address__contains=q)
        return {'q': q,
                'owners_fio': owners_fio,
                'owners_address': owners_address, }


class ParamCreateView(generic.CreateView):
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk', None)
        if pk:
            initial['_pk'] = pk
        return initial


class NoConfirmDeleteView(generic.DeleteView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class AjaxRequest:
    @classmethod
    def get_ajax(cls, request):
        if request.user.is_authenticated:
            if request.is_ajax():
                kwargs = request.GET.dict()
                result = list(cls.get_queryset_value(kwargs))
                data = json.dumps(result)
            else:
                data = 'fail'
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

    @staticmethod
    def get_queryset_value(kwarg: dict) -> QuerySet:
        pass


class OwnerView:
    class Create(AuthRequireView, generic.CreateView):
        form_class = forms.OwnerForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(AuthRequireView, generic.DetailView):
        model = models.Owner
        template_name = 'vet/owner/detail.html'

    class List(AuthRequireView, generic.ListView):
        model = models.Owner
        template_name = 'vet/owner/list.html'

    class Update(AuthRequireView, generic.UpdateView):
        form_class = forms.OwnerForm
        model = models.Owner
        template_name = 'vet/generic/generic_form.html'

    class Delete(AuthRequireView, NoConfirmDeleteView):
        model = models.Owner
        success_url = reverse_lazy('vet:owner-list')


class AnimalView:
    class Create(AuthRequireView, ParamCreateView):
        form_class = forms.AnimalForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(AuthRequireView, generic.DetailView):
        model = models.Animal
        template_name = 'vet/animal/detail.html'

    class List(AuthRequireView, generic.ListView):
        model = models.Animal
        template_name = 'vet/animal/list.html'

    class Update(AuthRequireView, generic.UpdateView):
        form_class = forms.AnimalForm
        model = models.Animal
        template_name = 'vet/generic/generic_form.html'

    class Delete(AuthRequireView, NoConfirmDeleteView):
        model = models.Animal

        def get_success_url(self):
            owner_pk = self.object.owner.pk
            return reverse_lazy('vet:owner-detail', kwargs={'pk': owner_pk})


class PreventionView:
    class Create(AuthRequireView, ParamCreateView):
        form_class = forms.PreventionForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(AuthRequireView, generic.DetailView):
        model = models.Prevention
        template_name = 'vet/prevention/detail.html'

    class List(AuthRequireView, generic.ListView):
        model = models.Prevention
        template_name = 'vet/prevention/list.html'

    class Update(AuthRequireView, generic.UpdateView):
        form_class = forms.PreventionForm
        model = models.Prevention
        template_name = 'vet/generic/generic_form.html'

    class Delete(AuthRequireView, NoConfirmDeleteView):
        model = models.Prevention

        def get_success_url(self):
            animal_pk = self.object.animal.pk
            return reverse_lazy('vet:animal-detail', kwargs={'pk': animal_pk})


class TherapyView:
    class Create(AuthRequireView, ParamCreateView):
        form_class = forms.TherapyForm
        template_name = 'vet/generic/generic_form.html'

    class Detail(AuthRequireView, generic.DetailView):
        model = models.Therapy
        template_name = 'vet/therapy/detail.html'

    class List(AuthRequireView, generic.ListView):
        model = models.Therapy
        template_name = 'vet/therapy/list.html'

    class Update(AuthRequireView, generic.UpdateView):
        form_class = forms.TherapyForm
        model = models.Therapy
        template_name = 'vet/generic/generic_form.html'

    class Delete(AuthRequireView, NoConfirmDeleteView):
        model = models.Therapy

        def get_success_url(self):
            animal_pk = self.object.animal.pk
            return reverse_lazy('vet:animal-detail', kwargs={'pk': animal_pk})


class DiagnosisView:
    @staticmethod
    @login_required
    def create(request):
        value = request.GET['value']
        models.Diagnosis.objects.get_or_create(value=value)
        return HttpResponse('')

    @staticmethod
    @login_required
    def update(request, pk):
        value = request.GET['value']
        diagnosis = get_object_or_404(models.Diagnosis, pk=pk)
        diagnosis.value = value
        diagnosis.save()
        return HttpResponse('')

    class List(AuthRequireView, generic.ListView):
        model = models.Diagnosis
        template_name = 'vet/diagnosis/list.html'

    @staticmethod
    @login_required
    def delete(request, pk):
        diagnosis = get_object_or_404(models.Diagnosis, pk=pk)
        diagnosis.delete()
        return HttpResponse('')


class VaccinationView:
    @staticmethod
    @login_required
    def create(request):
        value = request.GET['value']
        models.Vaccination.objects.get_or_create(value=value)
        return HttpResponse('')

    @staticmethod
    @login_required
    def update(request, pk):
        value = request.GET['value']
        vaccination = get_object_or_404(models.Vaccination, pk=pk)
        vaccination.value = value
        vaccination.save()
        return HttpResponse('')

    class List(AuthRequireView, generic.ListView):
        model = models.Vaccination
        template_name = 'vet/vaccination/list.html'

    @staticmethod
    @login_required
    def delete(request, pk):
        vaccination = get_object_or_404(models.Vaccination, pk=pk)
        vaccination.delete()
        return HttpResponse('')


class SpeciesSubspeciesView:
    @staticmethod
    @login_required
    def create(request):
        species_str = request.GET['species']
        subspecies_str = request.GET['subspecies']

        species, c = models.Species.objects.get_or_create(value=species_str)
        subspecies, c = models.Subspecies.objects.get_or_create(value=subspecies_str, species=species)

        return HttpResponse('')

    @staticmethod
    @login_required
    def update(request, pk):
        species_str = request.GET['species']
        subspecies_str = request.GET['subspecies']

        species, c = models.Species.objects.get_or_create(value=species_str)
        subspecies, c = models.Subspecies.objects.get_or_create(value=subspecies_str, species=species)

        value = request.GET['value']
        vaccination = get_object_or_404(models.Vaccination, pk=pk)
        vaccination.value = value
        vaccination.save()
        return HttpResponse('')

    class List(AuthRequireView, generic.ListView):
        template_name = 'vet/species_subspecies/list.html'
        model = models.Subspecies

    @staticmethod
    @login_required
    def delete(request, pk):
        return HttpResponse('')


class Ajax:
    class Owner(AjaxRequest):
        @staticmethod
        def get_queryset_value(kwarg):
            term = kwarg['term'].strip()
            owners = models.Owner.get_fio_address_by_term(term)[:10]
            list_out = [{'label': f'{owner.fio} {owner.address}', 'value': owner.pk} for owner in owners]
            return list_out

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

from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from . import forms
import json
import logging

logger = logging.getLogger(__name__)


class Species:
    @staticmethod
    def add_species(request, slug):
        models.Species.objects.get_or_create(value=slug)
        return HttpResponseRedirect(reverse_lazy('vet:owner-list'))


class Subspecies:
    @staticmethod
    def add_species(request, slug):
        pass


class Owner:
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


class Animal:
    class Create(generic.CreateView):
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


class Appointment:
    class Create(generic.CreateView):
        form_class = forms.AppointmentForm
        template_name = 'vet/appointment/form.html'

    class Detail(generic.DetailView):
        model = models.Appointment
        template_name = 'vet/appointment/detail.html'

    class List(generic.ListView):
        model = models.Appointment
        template_name = 'vet/appointment/list.html'

    class Update(generic.UpdateView):
        form_class = forms.AppointmentForm
        model = models.Appointment
        template_name = 'vet/appointment/form.html'

    class Delete(generic.DeleteView):
        model = models.Appointment
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:appointment-list')


class Ajax:
    @staticmethod
    def species(request):
        if request.is_ajax():
            q = request.GET['term']
            logger.info(q)
            result = list(models.Species.objects
                          .filter(value__icontains=q)[:10]
                          .values_list('value', flat=True))
            logger.info(result)

            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

    @staticmethod
    def subspecies(request):
        if request.is_ajax():

            # TODO Add species_ in filter of subspeies
            q = request.GET['term']
            logger.info(q)
            result = list(models.Subspecies.objects
                          .filter(value__icontains=q)[:10]
                          .values_list('value', flat=True))
            logger.info(result)

            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

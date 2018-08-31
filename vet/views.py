from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import Species, Owner, Animal, Subspecies, Appointment
from . import forms
import json
import logging

logger = logging.getLogger(__name__)

class OwnerView:
    class Create(generic.CreateView):
        form_class = forms.OwnerForm
        template_name = 'vet/owner/form.html'

    class Detail(generic.DetailView):
        model = Owner
        template_name = 'vet/owner/detail.html'

    class List(generic.ListView):
        model = Owner
        template_name = 'vet/owner/list.html'

    class Update(generic.UpdateView):
        form_class = forms.OwnerForm
        model = Owner
        template_name = 'vet/owner/form.html'

    class Delete(generic.DeleteView):
        model = Owner
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:owner-list')


class AnimalView:
    class Create(generic.CreateView):
        form_class = forms.AnimalForm
        template_name = 'vet/animal/form.html'

    class Detail(generic.DetailView):
        model = Animal
        template_name = 'vet/animal/detail.html'

    class List(generic.ListView):
        model = Animal
        template_name = 'vet/animal/list.html'

    class Update(generic.UpdateView):
        form_class = forms.AnimalForm
        model = Animal
        template_name = 'vet/animal/form.html'

        def get_initial(self):
            return {
                'owner': self.object.owner.fio,
                'species': self.object.species.value,
                'subspecies': self.object.subspecies.value,
            }

    class Delete(generic.DeleteView):
        model = Animal
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:animal-list')


class AppointmentView:
    class Create(generic.CreateView):
        form_class = forms.AppointmentForm
        template_name = 'vet/appointment/form.html'

    class Detail(generic.DetailView):
        model = Appointment
        template_name = 'vet/appointment/detail.html'

    class List(generic.ListView):
        model = Appointment
        template_name = 'vet/appointment/list.html'

    class Update(generic.UpdateView):
        form_class = forms.AppointmentForm
        model = Appointment
        template_name = 'vet/appointment/form.html'

    class Delete(generic.DeleteView):
        model = Appointment
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:appointment-list')


class Ajax:
    @staticmethod
    def species(request):
        if request.is_ajax():
            q = request.GET['term']

            result = list(Species.objects
                          .filter(value__icontains=q)[:10]
                          .values_list('value', flat=True))

            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

    @staticmethod
    def subspecies(request):
        if request.is_ajax():
            subspecies = request.GET['term']
            species = request.GET['term_2']

            result = list(Subspecies.objects
                          .filter(species__value=species)
                          .filter(value__icontains=subspecies)[:10]
                          .values_list('value', flat=True))
            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

    @staticmethod
    def owner(request):
        if request.is_ajax():
            q = request.GET['term']
            result = list(Owner.objects
                          .filter(fio__icontains=q)[:10]
                          .values_list('fio', flat=True))
            logger.info(result)

            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

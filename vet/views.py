from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Species, Owner, Animal, Subspecies, Appointment
from .forms import AnimalForm, AppointmentForm, OwnerForm
from django.http import HttpResponse
from django.urls import reverse_lazy
import json


class OwnerView:
    class Create(CreateView):
        form_class = OwnerForm
        template_name = 'vet/owner/form.html'

    class Detail(DetailView):
        model = Owner
        template_name = 'vet/owner/detail.html'

    class List(ListView):
        model = Owner
        template_name = 'vet/owner/list.html'

    class Update(UpdateView):
        form_class = OwnerForm
        model = Owner
        template_name = 'vet/owner/form.html'

    class Delete(DeleteView):
        model = Owner
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:owner-list')


class AnimalView:
    class Create(CreateView):
        form_class = AnimalForm
        template_name = 'vet/animal/form.html'

        def get_initial(self):
            initial = super().get_initial()
            try:
                owner = Owner.objects.get(pk=self.kwargs['owner_pk'])
                initial['owner'] = owner.fio
            except (KeyError, Owner.DoesNotExist):
                pass
            return initial

    class Detail(DetailView):
        model = Animal
        template_name = 'vet/animal/detail.html'

    class List(ListView):
        model = Animal
        template_name = 'vet/animal/list.html'

    class Update(UpdateView):
        form_class = AnimalForm
        model = Animal
        template_name = 'vet/animal/form.html'

        def get_initial(self):
            initial = super().get_initial()
            initial['owner'] = self.object.owner.fio
            initial['species'] = self.object.species.value
            initial['subspecies'] = self.object.subspecies.value
            return initial

    class Delete(DeleteView):
        model = Animal
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:animal-list')


class AppointmentView:
    class Create(CreateView):
        form_class = AppointmentForm
        template_name = 'vet/appointment/form.html'

    class Detail(DetailView):
        model = Appointment
        template_name = 'vet/appointment/detail.html'

    class List(ListView):
        model = Appointment
        template_name = 'vet/appointment/list.html'

    class Update(UpdateView):
        form_class = AppointmentForm
        model = Appointment
        template_name = 'vet/appointment/form.html'

    class Delete(DeleteView):
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

            data = json.dumps(result)
        else:
            data = 'fail'
        return HttpResponse(data, 'application/json')

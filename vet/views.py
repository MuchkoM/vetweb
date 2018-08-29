
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from . import models
from . import forms
import json


class Owner:
    class Create(generic.CreateView):
        form_class = forms.OwnerForm
        template_name = 'vet/owner/form.html'
        success_url = reverse_lazy('vet:owner-list')

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
        success_url = reverse_lazy('vet:owner-list')

    class Delete(generic.DeleteView):
        model = models.Owner
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:owner-list')


class Animal:
    class Create(generic.CreateView):
        form_class = forms.AnimalForm
        template_name = 'vet/animal/form.html'
        success_url = reverse_lazy('vet:animal-list')

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
        success_url = reverse_lazy('vet:animal-list')

    class Delete(generic.DeleteView):
        model = models.Animal
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:animal-list')


class Ajax:
    @staticmethod
    def species(request):
        if request.is_ajax():
            q = request.GET['term']
            result = list(models.Species.objects
                          .filter(genus__contains=q)
                          .distinct()
                          .values_list('genus', flat=True))
            data = json.dumps(result)
        else:
            data = 'fail'

        return HttpResponse(data, 'application/json')

    @staticmethod
    def subspecies(request):
        if request.is_ajax():
            q = request.GET.get('term', '')
            result = list(models.Animal.objects
                          .filter(genus__contains=q)
                          .distinct()
                          .values_list('genus', flat=True))
            data = json.dumps(result)
        else:
            data = 'fail'

        return HttpResponse(data, 'application/json')


class Appointment:
    class Create(generic.CreateView):
        form_class = forms.AppointmentForm
        template_name = 'vet/appointment/form.html'
        success_url = reverse_lazy('vet:appointment-list')

    class Detail(generic.DetailView):
        model = models.Appointment
        template_name = 'vet/appointment/detail.html'

    class List(generic.ListView):
        model = models.Appointment
        template_name = 'vet/appointment/list.html'

    class Update(generic.UpdateView):
        form_class = forms.AppointmentForm
        model = models.Appointment
        success_url = reverse_lazy('vet:appointment-list')
        template_name = 'vet/appointment/form.html'

    class Delete(generic.DeleteView):
        model = models.Appointment
        template_name = 'vet/generic/generic_confirm_delete.html'
        success_url = reverse_lazy('vet:appointment-list')




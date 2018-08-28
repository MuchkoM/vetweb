from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


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


class UserFormView(generic.View):
    form_class = forms.UserForm
    template_name = 'vet/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('vet:owner-list')

        return render(request, self.template_name, {"form": form})

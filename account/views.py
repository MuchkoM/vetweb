from django.views import generic
from django.urls import reverse_lazy
from .forms import UserForm


class UserFormView(generic.FormView):
    form_class = UserForm
    template_name = 'account/registration_form.html'
    success_url = reverse_lazy('vet:owner-list')

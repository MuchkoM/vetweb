from django.urls import path, include
from .views import Animal, Owner, Appointment, Ajax
from django.views.generic import RedirectView

app_name = 'vet'

url_owner = [
    path('', Owner.List.as_view(), name='owner-list'),
    path('create/', Owner.Create.as_view(), name='owner-create'),
    path('<int:pk>/', Owner.Detail.as_view(), name='owner-detail'),
    path('<int:pk>/update', Owner.Update.as_view(), name='owner-update'),
    path('<int:pk>/delete', Owner.Delete.as_view(), name='owner-delete'),
]
url_animal = [
    path('', Animal.List.as_view(), name='animal-list'),
    path('create/', Animal.Create.as_view(), name='animal-create'),
    path('<int:pk>/', Animal.Detail.as_view(), name='animal-detail'),
    path('<int:pk>/update', Animal.Update.as_view(), name='animal-update'),
    path('<int:pk>/delete', Animal.Delete.as_view(), name='animal-delete'),
]
url_appointment = [
    path('', Appointment.List.as_view(), name='appointment-list'),
    path('create/', Appointment.Create.as_view(), name='appointment-create'),
    path('<int:pk>/', Appointment.Detail.as_view(), name='appointment-detail'),
    path('<int:pk>/update', Appointment.Update.as_view(), name='appointment-update'),
    path('<int:pk>/delete', Appointment.Delete.as_view(), name='appointment-delete'),
]
url_ajax = [
    path('species/', Ajax.species, name='ajax-autocomplete-species'),
    path('subspecies/', Ajax.subspecies, name='ajax-autocomplete-subspecies'),
]

urlpatterns = [
    path('owner/', include(url_owner)),
    path('animal/', include(url_animal)),
    path('appointment/', include(url_appointment)),
    path('ajax/', include(url_ajax)),
    path('', RedirectView.as_view(pattern_name='vet:owner-list')),
]

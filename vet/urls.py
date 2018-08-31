from django.urls import path, include
from .views import AnimalView, OwnerView, AppointmentView, Ajax
from django.views.generic import RedirectView

app_name = 'vet'

url_owner = [
    path('', OwnerView.List.as_view(), name='owner-list'),
    path('create/', OwnerView.Create.as_view(), name='owner-create'),
    path('<int:pk>/', OwnerView.Detail.as_view(), name='owner-detail'),
    path('<int:pk>/update', OwnerView.Update.as_view(), name='owner-update'),
    path('<int:pk>/delete', OwnerView.Delete.as_view(), name='owner-delete'),
]
url_animal = [
    path('', AnimalView.List.as_view(), name='animal-list'),
    path('create/', AnimalView.Create.as_view(), name='animal-create'),
    path('<int:pk>/', AnimalView.Detail.as_view(), name='animal-detail'),
    path('<int:pk>/update', AnimalView.Update.as_view(), name='animal-update'),
    path('<int:pk>/delete', AnimalView.Delete.as_view(), name='animal-delete'),
]
url_appointment = [
    path('', AppointmentView.List.as_view(), name='appointment-list'),
    path('create/', AppointmentView.Create.as_view(), name='appointment-create'),
    path('<int:pk>/', AppointmentView.Detail.as_view(), name='appointment-detail'),
    path('<int:pk>/update', AppointmentView.Update.as_view(), name='appointment-update'),
    path('<int:pk>/delete', AppointmentView.Delete.as_view(), name='appointment-delete'),
]
url_ajax = [
    path('species/', Ajax.species, name='ajax-autocomplete-species'),
    path('subspecies/', Ajax.subspecies, name='ajax-autocomplete-subspecies'),
    path('owner/', Ajax.owner, name='ajax-autocomplete-owner'),
]

urlpatterns = [
    path('owner/', include(url_owner)),
    path('animal/', include(url_animal)),
    path('appointment/', include(url_appointment)),
    path('ajax/', include(url_ajax)),
    path('', RedirectView.as_view(pattern_name='vet:owner-list', permanent=False)),
]

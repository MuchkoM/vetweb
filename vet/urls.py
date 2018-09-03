from django.urls import path, include
from . import views
from django.views.generic import RedirectView

app_name = 'vet'

url_owner = [
    path('', views.OwnerView.List.as_view(), name='owner-list'),
    path('create/', views.OwnerView.Create.as_view(), name='owner-create'),
    path('<int:pk>/', views.OwnerView.Detail.as_view(), name='owner-detail'),
    path('<int:pk>/update', views.OwnerView.Update.as_view(), name='owner-update'),
    path('<int:pk>/delete', views.OwnerView.Delete.as_view(), name='owner-delete'),
]
url_animal = [
    path('', views.AnimalView.List.as_view(), name='animal-list'),
    path('create/', views.AnimalView.Create.as_view(), name='animal-create'),
    path('create/<int:pk>', views.AnimalView.Create.as_view(), name='animal-create-owner'),
    path('<int:pk>/', views.AnimalView.Detail.as_view(), name='animal-detail'),
    path('<int:pk>/update', views.AnimalView.Update.as_view(), name='animal-update'),
    path('<int:pk>/delete', views.AnimalView.Delete.as_view(), name='animal-delete'),
]
url_prevention = [
    path('', views.PreventionView.List.as_view(), name='prevention-list'),
    path('create/', views.PreventionView.Create.as_view(), name='prevention-create'),
    path('create/<int:pk>', views.PreventionView.Create.as_view(), name='prevention-create-animal'),
    path('<int:pk>/', views.PreventionView.Detail.as_view(), name='prevention-detail'),
    path('<int:pk>/update', views.PreventionView.Update.as_view(), name='prevention-update'),
    path('<int:pk>/delete', views.PreventionView.Delete.as_view(), name='prevention-delete'),
]
url_ajax = [
    path('species/', views.Ajax.Species.get_ajax, name='ajax-autocomplete-species'),
    path('subspecies/', views.Ajax.Subspecies.get_ajax, name='ajax-autocomplete-subspecies'),
    path('owner/', views.Ajax.Owner.get_ajax, name='ajax-autocomplete-owner'),
    path('vaccination/', views.Ajax.Vaccination.get_ajax, name='ajax-autocomplete-vaccination'),
    path('animal/', views.Ajax.Animal.get_ajax, name='ajax-autocomplete-animal'),
]

urlpatterns = [
    path('owner/', include(url_owner)),
    path('animal/', include(url_animal)),
    path('prevention/', include(url_prevention)),
    path('ajax/', include(url_ajax)),
    path('', RedirectView.as_view(pattern_name='vet:owner-list', permanent=False)),
]

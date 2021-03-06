from django.urls import path, include

from . import views

app_name = 'vet'

url_owner = [
    path('', views.OwnerView.List.as_view(), name='owner-list'),
    path('add/', views.OwnerView.Create.as_view(), name='owner-create'),
    path('<int:pk>/', views.OwnerView.Detail.as_view(), name='owner-detail'),
    path('<int:pk>/update', views.OwnerView.Update.as_view(), name='owner-update'),
    path('<int:pk>/delete', views.OwnerView.Delete.as_view(), name='owner-delete'),
]
url_animal = [
    path('', views.AnimalView.List.as_view(), name='animal-list'),
    path('add/', views.AnimalView.Create.as_view(), name='animal-create'),
    path('add/<int:pk>', views.AnimalView.Create.as_view(), name='animal-create-owner'),
    path('<int:pk>/', views.AnimalView.Detail.as_view(), name='animal-detail'),
    path('<int:pk>/update', views.AnimalView.Update.as_view(), name='animal-update'),
    path('<int:pk>/delete', views.AnimalView.Delete.as_view(), name='animal-delete'),
]
url_prevention = [
    path('', views.PreventionView.List.as_view(), name='prevention-list'),
    path('add/', views.PreventionView.Create.as_view(), name='prevention-create'),
    path('add/<int:pk>', views.PreventionView.Create.as_view(), name='prevention-create-animal'),
    path('<int:pk>/', views.PreventionView.Detail.as_view(), name='prevention-detail'),
    path('<int:pk>/update', views.PreventionView.Update.as_view(), name='prevention-update'),
    path('<int:pk>/delete', views.PreventionView.Delete.as_view(), name='prevention-delete'),
]
url_therapy = [
    path('', views.TherapyView.List.as_view(), name='therapy-list'),
    path('add/', views.TherapyView.Create.as_view(), name='therapy-create'),
    path('add/<int:pk>', views.TherapyView.Create.as_view(), name='therapy-create-animal'),
    path('<int:pk>/', views.TherapyView.Detail.as_view(), name='therapy-detail'),
    path('<int:pk>/update', views.TherapyView.Update.as_view(), name='therapy-update'),
    path('<int:pk>/delete', views.TherapyView.Delete.as_view(), name='therapy-delete'),
]
url_ajax = [
    path('owner/', views.Ajax.Owner.get_ajax, name='ajax-owner'),
    path('species/', views.Ajax.Species.get_ajax, name='ajax-species'),
    path('diagnosis/', views.Ajax.Diagnosis.get_ajax, name='ajax-diagnosis'),
    path('subspecies/', views.Ajax.Subspecies.get_ajax, name='ajax-subspecies'),
    path('vaccination/', views.Ajax.Vaccination.get_ajax, name='ajax-vaccination'),
]
url_diagnosis = [
    path('add/', views.diagnosis_create, name='diagnosis-create'),
    path('', views.DiagnosisList.as_view(), name='diagnosis-list'),
    path('update/<int:pk>', views.diagnosis_update, name='diagnosis-update'),
    path('delete/<int:pk>', views.diagnosis_delete, name='diagnosis-delete'),
]
url_vaccination = [
    path('add/', views.vaccination_create, name='vaccination-create'),
    path('', views.VaccinationList.as_view(), name='vaccination-list'),
    path('update/<int:pk>', views.vaccination_update, name='vaccination-update'),
    path('delete/<int:pk>', views.vaccination_delete, name='vaccination-delete'),
]
url_subspecies = [
    path('add/', views.subspecies_create, name='subspecies-create'),
    path('', views.SubspeciesList.as_view(), name='subspecies-list'),
    path('update/<int:pk>', views.subspecies_update, name='subspecies-update'),
    path('delete/<int:pk>', views.subspecies_delete, name='subspecies-delete'),
]
urlpatterns = [
    path('ajax/', include(url_ajax)),
    path('owner/', include(url_owner)),
    path('animal/', include(url_animal)),
    path('therapy/', include(url_therapy)),
    path('diagnosis/', include(url_diagnosis)),
    path('prevention/', include(url_prevention)),
    path('subspecies/', include(url_subspecies)),
    path('vaccination/', include(url_vaccination)),
    path('search/', views.SearchView.as_view(), name='search'),
]

from django.contrib.auth import views as auth_view
from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]

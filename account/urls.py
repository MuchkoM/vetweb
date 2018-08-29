from django.urls import path
from .views import UserFormView

app_name = 'account'

urlpatterns = [
    path('register/', UserFormView.as_view(), name='user-register'),
    path('logout/', UserFormView.as_view(), name='user-logout')
]

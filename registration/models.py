from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.db import models
# Create your models here.


class User(AbstractUser):
    class Meta:
        permissions = (
            ("full_access", _("To provide AC-Bus facility")),
            ("search_access", _("To provide AC-Bus facility")),
            ("no_access", _("To provide non-AC Bus facility")),
        )